---
id: 002
title: Phase 2 Implementation Plan
stage: plan
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5
feature: 002-phase2-fullstack-todo
branch: 002-phase2-fullstack-todo
user: HP
command: /sp.plan
labels: ["planning", "architecture", "monorepo", "fastapi", "nextjs", "postgresql", "authentication"]
links:
  spec: specs/002-phase2-fullstack-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase2-fullstack-todo/plan.md
  - specs/002-phase2-fullstack-todo/research.md
  - specs/002-phase2-fullstack-todo/data-model.md
  - specs/002-phase2-fullstack-todo/contracts/api-spec.yaml
  - specs/002-phase2-fullstack-todo/quickstart.md
tests:
  - N/A (planning artifacts)
---

## Prompt

```text
Architect a Monorepo solution for this specification.

## Tech Stack Constraints (MANDATORY)
1. **Structure:** Monorepo with `/frontend` (Next.js 16 App Router) and `/backend` (Python FastAPI).
2. **Database:** Neon Serverless PostgreSQL using **SQLModel** (Python).
3. **Authentication Architecture:**
   - Frontend: Use **Better Auth** for Signup/Login.
   - Integration: Frontend attaches **JWT Token** to all API requests.
   - Backend: FastAPI Middleware validates JWT using a shared `BETTER_AUTH_SECRET`.
4. **API Strategy:**
   - FastAPI exposes REST endpoints at `/api/{user_id}/tasks`.
   - Next.js uses Server Actions or fetch to call FastAPI.

## Critical Deliverables in Plan
- Define the exact SQLModel schema for `User` and `Task`.
- Define the folder structure for the monorepo.
- Define the Docker/Compose setup for local development.
```

## Response snapshot

**Planning Complete**: Comprehensive implementation plan with all required artifacts

**Artifacts Generated**:

1. **research.md** (Phase 0):
   - 6 key technology decisions researched and justified
   - Alternatives considered for each decision
   - Monorepo structure, Better Auth + JWT integration, SQLModel schema strategy, API endpoint design, Docker Compose config, Next.js Server Actions
   - All decisions comply with Constitution v2.0.0

2. **data-model.md** (Phase 1):
   - Complete SQLModel schemas for User and Task entities
   - User: `id` (PK), `email` (unique, indexed), `hashed_password`, `created_at`
   - Task: `id` (PK), `title`, `description`, `is_complete`, `created_at`, `updated_at`, `user_id` (FK, indexed)
   - Foreign key cascade delete strategy
   - Alembic migration strategy with initial migration code
   - Query patterns for all CRUD operations with authorization checks
   - Performance considerations: connection pooling, index strategy

3. **contracts/api-spec.yaml** (Phase 1):
   - OpenAPI 3.0 specification for all 8 endpoints
   - Authentication: `/auth/register`, `/auth/login`
   - Tasks: 6 RESTful endpoints at `/api/v1/users/{user_id}/tasks`
   - Complete request/response schemas
   - Error responses (400, 401, 403, 404)
   - Security scheme: Bearer JWT authentication

4. **quickstart.md** (Phase 1):
   - Docker Compose setup (recommended path)
   - Local development without Docker (alternative)
   - Complete docker-compose.yml configuration
   - Backend Dockerfile (Python 3.13 + UV)
   - Frontend Dockerfile (Node 20)
   - Common tasks: migrations, logs, tests, linting
   - Troubleshooting guide
   - Environment variables reference

5. **plan.md** (Implementation Plan):
   - Technical context (languages, dependencies, constraints)
   - Constitution Check: ✅ All 7 principles satisfied
   - Complete monorepo project structure (backend and frontend)
   - Phase 0 and Phase 1 status: COMPLETE
   - Implementation strategy: MVP-first (P1 stories), parallel development opportunities
   - Risk analysis: Top 3 risks with mitigations
   - Testing strategy: contract, integration, unit, E2E tests
   - Success criteria traceability

**Key Architectural Decisions**:

1. **SQLModel Schema**:
   ```python
   class User(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       email: str = Field(unique=True, index=True, max_length=255)
       hashed_password: str = Field(max_length=255)
       created_at: datetime = Field(default_factory=datetime.utcnow)
       tasks: List["Task"] = Relationship(back_populates="user")

   class Task(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       title: str = Field(max_length=200)
       description: Optional[str] = Field(default=None, max_length=2000)
       is_complete: bool = Field(default=False)
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)
       user_id: int = Field(foreign_key="users.id", index=True)
       user: User = Relationship(back_populates="tasks")
   ```

2. **Monorepo Structure**:
   - `/backend`: FastAPI with src/models, src/services, src/api, src/auth
   - `/frontend`: Next.js with src/app (App Router), src/components, src/lib
   - Docker Compose: postgres, backend, frontend services

3. **Authentication Flow**:
   - Better Auth (frontend) generates JWT with `BETTER_AUTH_SECRET`
   - FastAPI middleware validates JWT, extracts `user_id`
   - Every API endpoint checks `user_id` matches authenticated user (403 if not)

**Constitution Compliance**: ✅ All 7 principles validated pre- and post-design

## Outcome

- ✅ Impact: Complete architectural plan ready for `/sp.tasks` command, with detailed technology decisions, database schema, API contracts, and local development setup
- 🧪 Tests: N/A (planning artifacts)
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, contracts/api-spec.yaml, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks organized by user story (P1, P2, P3); Consider ADR for monorepo architecture decision; Review quickstart.md and test Docker Compose setup
- 🧠 Reflection: Planning workflow complete with all Phase 0 and Phase 1 artifacts. SQLModel schemas are production-ready with proper indexes and relationships. OpenAPI contract enables parallel frontend/backend development. Docker Compose provides turnkey local development.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts generated successfully
- Graders run and results (PASS/FAIL): Constitution Check PASS (7/7 principles, both pre- and post-design), Completeness Check PASS (all critical deliverables met)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): During `/sp.tasks`, evaluate whether to split authentication tasks into separate "User Service" phase before task CRUD implementation
