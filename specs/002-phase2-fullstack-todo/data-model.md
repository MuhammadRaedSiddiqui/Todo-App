# Data Model: Phase 2 Full-Stack Todo App

**Feature**: 002-phase2-fullstack-todo
**Date**: 2026-01-05
**Purpose**: Define database schema and entity relationships using SQLModel

## Entity Overview

```
User (1) ──────< (Many) Task
```

- One User can have zero or many Tasks
- Each Task belongs to exactly one User
- Relationship enforced via foreign key constraint

---

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user account with authentication credentials

**SQLModel Schema**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    """User account for authentication and task ownership."""

    __tablename__ = "users"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing user ID"
    )

    # Authentication
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address (unique, indexed for login queries)"
    )

    hashed_password: str = Field(
        max_length=255,
        description="Bcrypt hashed password (never store plaintext)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Primary Key, Auto-increment | Unique user identifier |
| `email` | `str` | Unique, Indexed, Max 255 chars | User login email (FR-001, FR-002) |
| `hashed_password` | `str` | Max 255 chars | Bcrypt hash of password (FR-004) |
| `created_at` | `datetime` | Not null, Default UTC now | Account creation timestamp |
| `tasks` | `List[Task]` | Relationship | User's tasks (cascade delete) |

**Validation Rules**:
- Email: Must be valid email format (validated by Better Auth on frontend)
- Password: Minimum 8 characters before hashing (FR-003)
- Email uniqueness enforced at database level (unique constraint)

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for fast login lookups)

**Security**:
- Password stored as bcrypt hash with salt (never plaintext)
- Cascade delete: Deleting user removes all their tasks

---

### Task Entity

**Purpose**: Represents a single todo item owned by a user

**SQLModel Schema**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Todo task with user ownership and completion tracking."""

    __tablename__ = "tasks"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing task ID"
    )

    # Task Content
    title: str = Field(
        max_length=200,
        description="Task title (required, max 200 chars per FR-010)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional, max 2000 chars per FR-011)"
    )

    # Status
    is_complete: bool = Field(
        default=False,
        description="Completion status (default incomplete per FR-018)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (UTC, per FR-013)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

    # Foreign Key (User Ownership)
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID (indexed for user-scoped queries per FR-021)"
    )

    # Relationships
    user: User = Relationship(back_populates="tasks")
```

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Primary Key, Auto-increment | Unique task identifier (FR-012) |
| `title` | `str` | Not null, Max 200 chars | Task title (FR-010) |
| `description` | `str \| None` | Nullable, Max 2000 chars | Task description (FR-011) |
| `is_complete` | `bool` | Not null, Default `False` | Completion status (FR-017, FR-018) |
| `created_at` | `datetime` | Not null, Default UTC now | Creation timestamp (FR-013) |
| `updated_at` | `datetime` | Not null, Default UTC now | Last update timestamp |
| `user_id` | `int` | Foreign Key to `users.id`, Indexed | Owner user ID (FR-021) |
| `user` | `User` | Relationship | Owner user object |

**Validation Rules**:
- Title: Required, max 200 characters (enforced at model level)
- Description: Optional, max 2000 characters if provided
- User ID: Must reference existing user (foreign key constraint)

**Indexes**:
- Primary key index on `id` (automatic)
- **Critical**: Index on `user_id` for fast user-scoped queries (FR-021 compliance)
- Combined index on `(user_id, created_at)` for optimized list queries with sorting

**State Transitions**:
```
[Created] ──────> is_complete = False (default)
           ↓
[Toggle Complete] ──> is_complete = True
           ↓
[Toggle Incomplete] ──> is_complete = False
```

---

## Database Constraints

### Foreign Key Constraints

```sql
ALTER TABLE tasks
  ADD CONSTRAINT fk_task_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE;
```

**Rationale**: Cascading delete ensures orphaned tasks are automatically removed when user is deleted.

### Unique Constraints

```sql
ALTER TABLE users
  ADD CONSTRAINT uq_user_email
  UNIQUE (email);
```

**Rationale**: Enforces one account per email address at database level (FR-001).

---

## Pydantic Models (API Schemas)

### Request/Response Models

**User Registration Request**:
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Request body for user registration."""
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
```

**Task Create Request**:
```python
class TaskCreate(BaseModel):
    """Request body for creating a task."""
    title: str = Field(..., max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
```

**Task Update Request**:
```python
class TaskUpdate(BaseModel):
    """Request body for updating a task."""
    title: Optional[str] = Field(None, max_length=200, description="Updated title")
    description: Optional[str] = Field(None, max_length=2000, description="Updated description")
```

**Task Response**:
```python
class TaskRead(BaseModel):
    """Response body for task operations."""
    id: int
    title: str
    description: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
```

---

## Migration Strategy

### Initial Migration (Alembic)

**File**: `backend/alembic/versions/001_initial_schema.py`

```python
"""Initial schema: users and tasks tables

Revision ID: 001
Create Date: 2026-01-05
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('is_complete', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_created', 'tasks', ['user_id', 'created_at'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

**Migration Commands**:
```bash
# Generate migration (if using autogenerate)
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Query Patterns

### User-Scoped Task Queries

**List all tasks for user** (FR-015):
```python
from sqlmodel import select

# Optimized query with user_id index
tasks = session.exec(
    select(Task)
    .where(Task.user_id == current_user.id)
    .order_by(Task.created_at.desc())  # FR-014: newest first
).all()
```

**Get single task with authorization check** (FR-016, FR-022):
```python
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user.id)  # Authorization filter
).first()

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Create task** (FR-009):
```python
new_task = Task(
    title=task_data.title,
    description=task_data.description,
    user_id=current_user.id  # Set ownership
)
session.add(new_task)
session.commit()
session.refresh(new_task)
```

**Update task** (FR-019, FR-023):
```python
task = session.get(Task, task_id)
if task.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Access forbidden")

task.title = task_data.title
task.description = task_data.description
task.updated_at = datetime.utcnow()
session.commit()
```

**Toggle completion** (FR-017, FR-018):
```python
task = session.get(Task, task_id)
if task.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Access forbidden")

task.is_complete = not task.is_complete
task.updated_at = datetime.utcnow()
session.commit()
```

**Delete task** (FR-020, FR-024):
```python
task = session.get(Task, task_id)
if task.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Access forbidden")

session.delete(task)
session.commit()
```

---

## Performance Considerations

### Index Strategy

1. **Users Table**:
   - Primary key index on `id` (automatic)
   - Unique index on `email` (login queries)

2. **Tasks Table**:
   - Primary key index on `id` (automatic)
   - **Critical**: Index on `user_id` (all task queries filter by user)
   - Composite index on `(user_id, created_at)` (list queries with sorting)

**Query Performance Estimates** (for 100 tasks per user):
- List tasks: ~2ms with `user_id` index
- Get single task: ~1ms with primary key lookup
- User login: ~1ms with email index

### Connection Pooling

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Max 10 connections
    max_overflow=20,        # Up to 30 total connections under load
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600       # Recycle connections after 1 hour
)
```

---

## Constitution Compliance

This data model complies with:

- **Principle II**: Neon PostgreSQL with SQLModel ORM ✅
- **Principle VI**: RESTful data access via API endpoints ✅
- **Principle VII**: User-scoped data with `user_id` foreign key ✅

All functional requirements (FR-001 through FR-031) are satisfied by this schema.
