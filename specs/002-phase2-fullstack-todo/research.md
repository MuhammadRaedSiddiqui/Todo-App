# Research: Phase 2 Full-Stack Todo App

**Feature**: 002-phase2-fullstack-todo
**Date**: 2026-01-05
**Purpose**: Technology research and architectural decisions for monorepo implementation

## Research Areas

### 1. Monorepo Structure for Next.js + FastAPI

**Decision**: Use workspace-based monorepo with separate frontend and backend directories at repository root

**Rationale**:
- Constitution v2.0.0 Principle III mandates `/frontend` and `/backend` separation
- Each workspace maintains independent dependency management (npm for frontend, UV for backend)
- Simplifies deployment: frontend and backend can be deployed independently
- Enables atomic commits across full stack when API contracts change
- Industry standard: widely adopted by teams using polyglot stacks

**Alternatives Considered**:
- **Turborepo/Nx**: More complex tooling, overkill for two-workspace monorepo
- **Git submodules**: Adds complexity, harder to maintain atomic commits
- **Separate repositories**: Violates Constitution mandate, complicates API contract sync

**Implementation Approach**:
```
/
├── frontend/          # Next.js 16+ workspace
│   ├── package.json
│   └── src/
├── backend/           # FastAPI workspace
│   ├── pyproject.toml
│   └── src/
├── specs/             # Shared specifications
└── docker-compose.yml # Local development orchestration
```

---

### 2. Better Auth + FastAPI JWT Integration

**Decision**: Use Better Auth for frontend authentication with JWT token exchange to FastAPI backend

**Architecture**:
1. **Frontend (Better Auth)**:
   - Handles signup/login UI flows
   - Manages JWT token generation using `BETTER_AUTH_SECRET`
   - Stores JWT in HTTP-only cookies for security
   - Automatically attaches JWT to all API requests via Authorization header

2. **Backend (FastAPI)**:
   - Validates JWT tokens using shared `BETTER_AUTH_SECRET`
   - Extracts `user_id` from verified JWT payload
   - Uses `user_id` for database query scoping
   - Returns 401 for invalid/missing tokens

**Rationale**:
- Constitution v2.0.0 Principle VII mandates JWT authentication
- Better Auth provides modern auth patterns with minimal configuration
- Shared secret approach is simpler than public key infrastructure for MVP
- Stateless JWT enables horizontal scaling (no server-side sessions)

**Alternatives Considered**:
- **Session-based auth**: Requires Redis/database for sessions, adds stateful dependency
- **OAuth2 with separate auth service**: Over-engineered for Phase 2, increases complexity
- **Magic link auth**: Better UX but requires email service (out of scope)

**Implementation Pattern**:
```python
# Backend: FastAPI dependency
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
    user_id = payload.get("sub")
    # Fetch user from database
    return user
```

**Security Considerations**:
- JWT tokens expire after 7 days (configurable)
- Shared secret stored in environment variables, never committed
- HTTPS required in production (Constitution mandate)
- Logout implemented by clearing cookie (client-side invalidation)

---

### 3. SQLModel Schema Design for User-Scoped Data

**Decision**: Use SQLModel with explicit `user_id` foreign key on Task table, indexed for query performance

**Schema Strategy**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key with index for user-scoped queries
    user_id: int = Field(foreign_key="users.id", index=True)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

**Rationale**:
- Explicit `user_id` foreign key enforces referential integrity at database level
- Index on `user_id` optimizes `WHERE user_id = ?` queries (every task read operation)
- SQLModel provides Pydantic validation + SQLAlchemy ORM in single definition
- `created_at` and `updated_at` timestamps satisfy audit requirements
- Max length constraints match spec requirements (FR-010, FR-011)

**Alternatives Considered**:
- **UUID for primary keys**: More secure but adds complexity, integer IDs sufficient for Phase 2
- **Soft deletes**: Adds `deleted_at` column, decided unnecessary for MVP
- **Separate audit table**: Over-engineered for Phase 2, timestamps sufficient

**Migration Strategy**:
- Use Alembic for database migrations
- Initial migration creates both tables with foreign key constraint
- Migrations versioned in `backend/alembic/versions/`

---

### 4. API Endpoint Design for User-Scoped Operations

**Decision**: Use RESTful endpoints at `/api/v1/users/{user_id}/tasks` with FastAPI dependency injection for user validation

**Endpoint Structure**:
```
GET    /api/v1/users/{user_id}/tasks           # List all tasks for user
POST   /api/v1/users/{user_id}/tasks           # Create task for user
GET    /api/v1/users/{user_id}/tasks/{task_id} # Get single task
PUT    /api/v1/users/{user_id}/tasks/{task_id} # Update task (full replace)
PATCH  /api/v1/users/{user_id}/tasks/{task_id}/complete  # Toggle completion
DELETE /api/v1/users/{user_id}/tasks/{task_id} # Delete task
```

**Security Pattern**:
```python
@router.get("/users/{user_id}/tasks")
async def list_tasks(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Validate user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    # Query with user_id filter
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

**Rationale**:
- `/api/v1/` prefix enables future versioning (Constitution Principle VI)
- `user_id` in path makes authorization explicit and self-documenting
- FastAPI dependency injection cleanly separates auth logic from business logic
- 403 Forbidden for user_id mismatch (user is authenticated but not authorized)
- 401 Unauthorized for missing/invalid JWT (authentication failure)

**Alternatives Considered**:
- **Implicit user from JWT only**: `/api/v1/tasks` (simpler but less explicit)
  - Decided against: spec explicitly requires `user_id` in path
- **GraphQL**: More flexible but adds complexity, REST sufficient for CRUD
- **PATCH for all updates**: Decided to use PUT for full updates, PATCH only for completion toggle

---

### 5. Docker Compose for Local Development

**Decision**: Use Docker Compose to orchestrate Neon PostgreSQL (local), FastAPI backend, and Next.js frontend

**Compose Structure**:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: todo_dev
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    command: uvicorn src.main:app --host 0.0.0.0 --reload
    volumes:
      - ./backend:/app
    environment:
      DATABASE_URL: postgresql://todo_user:todo_pass@postgres:5432/todo_dev
      BETTER_AUTH_SECRET: dev-secret-change-in-production
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
      BETTER_AUTH_SECRET: dev-secret-change-in-production
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

**Rationale**:
- Single `docker compose up` command starts entire stack (DX optimization)
- PostgreSQL 16 for local development mimics Neon PostgreSQL version
- Volume mounts enable hot reload for both frontend and backend
- Environment variables centralized in compose file for dev (production uses .env files)
- Service dependencies ensure correct startup order

**Alternatives Considered**:
- **Neon database for local dev**: Requires internet, slower feedback loop
- **Separate docker run commands**: More error-prone, harder to document
- **No Docker (native installs)**: Inconsistent environments across team members

**Production Deployment** (out of scope for plan, but noted):
- Frontend: Vercel or similar edge platform
- Backend: Docker container on cloud platform (AWS ECS, Google Cloud Run, etc.)
- Database: Neon Serverless PostgreSQL (managed)

---

### 6. Next.js Server Actions vs. Client-Side Fetch

**Decision**: Use Next.js Server Actions for authenticated API calls to FastAPI backend

**Pattern**:
```typescript
// app/actions/tasks.ts
'use server'

import { cookies } from 'next/headers'

export async function createTask(formData: FormData) {
  const token = cookies().get('auth_token')?.value

  const response = await fetch(`${process.env.API_URL}/users/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: formData.get('title'),
      description: formData.get('description')
    })
  })

  if (!response.ok) {
    throw new Error('Failed to create task')
  }

  revalidatePath('/tasks')
  return await response.json()
}
```

**Rationale**:
- Server Actions run on server, preventing token exposure to browser
- Automatic revalidation with `revalidatePath()` keeps UI in sync
- Better integration with Next.js 16 App Router patterns
- Simplifies loading states with React `useTransition` hook

**Alternatives Considered**:
- **Client-side fetch with React Query**: More boilerplate, token management in browser
- **Next.js API routes as proxy**: Extra indirection, unnecessary latency
- **tRPC**: Over-engineered for REST API, adds learning curve

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Monorepo Structure** | `/frontend` and `/backend` workspaces at root | Constitution mandate, independent deployments |
| **Authentication** | Better Auth (frontend) + JWT validation (backend) | Stateless, scalable, Constitution Principle VII |
| **Database Schema** | SQLModel with indexed `user_id` foreign key | Type-safe, performant user-scoped queries |
| **API Design** | REST with `/api/v1/users/{user_id}/tasks` | Explicit authorization, versioned, RESTful |
| **Local Dev** | Docker Compose with PostgreSQL 16 | Consistent environments, one-command startup |
| **API Calls** | Next.js Server Actions | Secure token handling, App Router integration |

All decisions comply with Constitution v2.0.0 Principles II, III, VI, and VII.
