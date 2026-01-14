# ADR-003: Data Persistence with Neon PostgreSQL and SQLModel

**Status**: Accepted
**Date**: 2026-01-05
**Deciders**: Architecture Team, Database Team
**Feature**: 002-phase2-fullstack-todo

## Context

Phase 2 requires persistent multi-user task storage. Key requirements:

1. **User-Scoped Data** (FR-021-FR-027): Zero cross-user data access
2. **CRUD Operations** (FR-009-FR-020): Create, read, update, delete tasks
3. **Performance** (SC-003): Load 100 tasks in < 2 seconds
4. **Data Integrity** (FR-028-FR-031): Persist across restarts, handle failures gracefully
5. **Type Safety**: Python type hints for database models
6. **Constitution Compliance**: Principle II mandates Neon PostgreSQL + SQLModel ORM

**Constraints**:
- Phase 1 used in-memory storage (lists/dictionaries) - now **REVOKED** by Constitution v2.0.0
- Must support 100-1000 concurrent users initially
- Database must be managed (no manual PostgreSQL administration)
- Migration strategy for schema evolution

## Decision

Adopt **Neon Serverless PostgreSQL + SQLModel ORM** with the following architecture:

### Technology Stack

**Database**: Neon Serverless PostgreSQL 16+
- Fully managed cloud PostgreSQL
- Serverless architecture (auto-scaling, auto-pause)
- Built-in connection pooling
- Branch-based development databases

**ORM**: SQLModel 0.0.22+
- Combines SQLAlchemy (ORM) + Pydantic (validation)
- Single model definition for database and API schemas
- Type-safe queries with Python type hints
- Relationship management

**Migration Tool**: Alembic
- Database schema versioning
- Auto-generate migrations from model changes
- Rollback capabilities

### Database Schema

**User Entity**:
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Task Entity**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key with index (CRITICAL for user-scoped queries)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

### Indexing Strategy

**Critical Indexes**:
1. **`users.email`**: Unique index for fast login queries
2. **`tasks.user_id`**: Non-unique index for user-scoped queries (EVERY task read filters by this)
3. **`tasks (user_id, created_at)`**: Composite index for sorted task lists

**Query Performance**:
- List tasks for user: ~2ms with `user_id` index (100 tasks)
- Get single task: ~1ms with primary key lookup
- User login: ~1ms with email index

### User-Scoped Query Pattern

**Every task query MUST filter by `user_id`**:
```python
# List tasks - CORRECT
tasks = session.exec(
    select(Task)
    .where(Task.user_id == current_user.id)  # User-scoped filter
    .order_by(Task.created_at.desc())
).all()

# Get task - CORRECT (with authorization check)
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user.id)  # Prevents cross-user access
).first()

if not task:
    raise HTTPException(status_code=404)  # Not found OR not authorized
```

### Connection Pooling

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Max 10 connections
    max_overflow=20,        # Up to 30 total under load
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600       # Recycle after 1 hour
)
```

## Consequences

### Positive

✅ **Constitution Compliance**: Satisfies Principle II mandate for Neon PostgreSQL + SQLModel

✅ **Type Safety**: SQLModel provides Pydantic validation + SQLAlchemy ORM in single definition, reducing bugs

✅ **Managed Infrastructure**: Neon handles backups, scaling, high availability - no DBA required

✅ **Auto-Scaling**: Neon serverless architecture scales storage and compute independently

✅ **Cost Efficiency**: Auto-pause when idle (development databases), pay-per-use model

✅ **Fast Development**: Branch-based databases for feature development (one database per feature branch)

✅ **Security**: User-scoped queries enforced at database level with foreign keys, indexed for performance

✅ **Migration Safety**: Alembic migrations are version-controlled, reviewable, and reversible

### Negative

⚠️ **Vendor Lock-In**: Neon-specific features (branching, serverless) make migration to self-hosted PostgreSQL harder
- **Mitigation**: Standard PostgreSQL underneath, can export to any PostgreSQL provider

⚠️ **Cold Start Latency**: Serverless databases can have 1-2 second cold start after idle period
- **Mitigation**: Keep-alive queries, production databases rarely idle, configurable auto-pause

⚠️ **Connection Limits**: Neon has connection limits based on plan tier
- **Mitigation**: Connection pooling (max 30), async queries, pgBouncer if needed

⚠️ **Migration Complexity**: Alembic auto-generate can miss complex schema changes
- **Mitigation**: Review all migrations before applying, test against staging database

### Risks

🔴 **Risk**: Cross-user data access bug (privacy violation)
- **Mitigation**: Index on `user_id`, explicit filter in every query, integration tests verify 403 errors

🟡 **Risk**: Database connection pool exhaustion under high load
- **Mitigation**: Connection pool limits (30), async queries, monitoring alerts, horizontal backend scaling

🟢 **Risk**: Schema migration failures during deployment
- **Mitigation**: Blue-green deployment, rollback plan, test migrations on staging first

## Alternatives Considered

### Alternative 1: MySQL + Raw SQLAlchemy

**Pros**:
- More mature ecosystem than PostgreSQL
- Wide industry adoption
- Familiar to many developers

**Cons**:
- **Violates Constitution**: Principle II mandates PostgreSQL
- Lacks advanced PostgreSQL features (JSONB, arrays, full-text search)
- Raw SQLAlchemy requires more boilerplate (separate Pydantic models)

**Why Rejected**: Constitution violation is a blocker. SQLModel's Pydantic integration provides superior DX.

### Alternative 2: MongoDB + Motor (Async MongoDB Driver)

**Pros**:
- Schemaless flexibility
- Horizontal scaling built-in (sharding)
- Native JSON storage

**Cons**:
- **Violates Constitution**: Principle II mandates SQL database (PostgreSQL)
- No foreign key constraints (user-scoped queries harder to enforce)
- Lacks ACID transactions for complex operations
- Requires learning MongoDB query language

**Why Rejected**: Constitution violation. Relational model better fits user-task relationships. ACID guarantees simplify error handling.

### Alternative 3: Self-Hosted PostgreSQL on AWS RDS

**Pros**:
- No vendor lock-in (standard PostgreSQL)
- Full control over configuration
- Predictable pricing (no serverless surprises)

**Cons**:
- **Operational Burden**: Manual backups, scaling, monitoring, security patches
- **No Branching**: Can't easily create per-feature databases
- **Higher Baseline Cost**: Always-on instances more expensive for low traffic
- **DBA Required**: Need database administration expertise

**Why Rejected**: Neon's managed features (branching, auto-scaling, backups) align better with small team needs. Can migrate to RDS later if needed.

### Alternative 4: SQLite + Litestream (Distributed SQLite)

**Pros**:
- Simplest possible setup (single file database)
- Zero network latency (embedded)
- Litestream provides replication

**Cons**:
- **Single-Writer Limitation**: Cannot handle concurrent writes (100+ users requirement)
- **No Connection Pooling**: Embedded database, can't distribute load
- **Scaling Challenges**: Difficult to scale beyond single server
- **Production Risk**: SQLite not designed for multi-user web apps

**Why Rejected**: Cannot meet 100 concurrent user requirement. SQLite is excellent for embedded/local-first apps but inappropriate for multi-user web backend.

## Implementation Details

### Database URL Configuration

```python
# backend/src/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Format: postgresql://user:pass@host:port/dbname
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    class Config:
        env_file = ".env"

settings = Settings()
```

### SQLModel Session Management

```python
# backend/src/core/database.py
from sqlmodel import Session, create_engine

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

def get_session():
    """FastAPI dependency for database sessions."""
    with Session(engine) as session:
        yield session
```

### Alembic Migration Example

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add tasks table"

# Review migration file (ALWAYS review auto-generated)
# backend/alembic/versions/001_add_tasks_table.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## References

- [Constitution v2.0.0 Principle II](../../.specify/memory/constitution.md#principle-ii-persistence-layer-with-neon-postgresql)
- [Data Model: SQLModel Schemas](../../specs/002-phase2-fullstack-todo/data-model.md)
- [Research: SQLModel Schema Design](../../specs/002-phase2-fullstack-todo/research.md#3-sqlmodel-schema-design-for-user-scoped-data)
- [Neon PostgreSQL Documentation](https://neon.tech/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)

## Notes

- **Reversibility**: High difficulty. Switching databases requires data migration, schema conversion, query rewrites
- **Future Enhancements**: Full-text search on task titles, soft deletes (deleted_at column), audit logs
- **Monitoring**: Set up alerts for connection pool utilization, slow queries (> 100ms), failed transactions
- **Backup Strategy**: Neon provides automated backups (7-day retention default), document restore procedure
