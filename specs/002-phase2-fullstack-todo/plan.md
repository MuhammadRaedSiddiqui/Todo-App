# Implementation Plan: Phase 2 Full-Stack Todo App

**Branch**: `002-phase2-fullstack-todo` | **Date**: 2026-01-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack-todo/spec.md`

## Summary

Phase 2 transforms the Todo App from a single-user CLI application to a full-stack multi-user web application. The monorepo architecture separates frontend (Next.js 16+ App Router) and backend (FastAPI) with Neon Serverless PostgreSQL for persistence. Better Auth handles user authentication with JWT tokens, and all task data is strictly scoped to authenticated users.

**Primary Requirement**: Multi-user todo application with secure authentication and user-isolated task data

**Technical Approach**:
1. **Monorepo Structure**: Independent frontend and backend workspaces with Docker Compose orchestration
2. **Authentication Flow**: Better Auth generates JWT tokens, FastAPI validates via shared secret
3. **Data Isolation**: SQLModel schema with indexed `user_id` foreign key enforces user-scoped queries
4. **API Design**: RESTful endpoints at `/api/v1/users/{user_id}/tasks` with explicit authorization checks
5. **Local Development**: Docker Compose provides turnkey development environment with hot reload

---

## Technical Context

**Language/Version**: Python 3.13+ (backend), Node.js 20+ / TypeScript 5.7+ (frontend)

**Primary Dependencies**:
- **Backend**: FastAPI 0.115+, SQLModel 0.0.22+, psycopg2-binary 2.9.10+, python-jose 3.3.0+, passlib 1.7.4+
- **Frontend**: Next.js 16+, React 19, Better Auth 1.0+, Tailwind CSS 4.0+

**Storage**: Neon Serverless PostgreSQL 16+ (managed cloud database)

**Testing**:
- **Backend**: pytest 8.3+, pytest-asyncio 0.24+, httpx 0.28+ (for API testing)
- **Frontend**: Jest, React Testing Library, Playwright (E2E)

**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)

**Project Type**: Monorepo web application (frontend + backend)

**Performance Goals**:
- Task list loads in < 2 seconds for 100 tasks
- Task create/update/delete operations complete in < 500ms
- Support 100 concurrent authenticated users
- 95% API success rate

**Constraints**:
- JWT tokens expire after 7 days (configurable)
- Task titles max 200 characters, descriptions max 2000 characters
- User-scoped data: zero cross-user data access allowed
- HTTPS required in production

**Scale/Scope**:
- Designed for 100-1000 users initially
- PostgreSQL indexed for efficient user-scoped queries
- Horizontal scaling via stateless JWT authentication

---

## Constitution Check

**Gate: Must pass before Phase 0 research. Re-check after Phase 1 design.**

### Principle I: Spec-Driven Development ✅ PASS
- Feature spec created: `specs/002-phase2-fullstack-todo/spec.md`
- Tasks will reference spec requirements (FR-001 through FR-031)
- All 5 user stories defined with acceptance criteria

### Principle II: Persistence Layer with Neon PostgreSQL ✅ PASS
- Neon Serverless PostgreSQL mandated
- SQLModel ORM for type-safe operations
- Database schema defined in `data-model.md`
- Migration strategy with Alembic

### Principle III: Monorepo Architecture with Multi-Technology Stack ✅ PASS
- `/frontend` workspace: Next.js 16+ App Router, Tailwind CSS
- `/backend` workspace: Python FastAPI, SQLModel, Neon PostgreSQL
- Independent dependency management (npm, UV)
- API contracts documented in `contracts/api-spec.yaml`

### Principle IV: Code Quality Standards ✅ PASS
- **Python**: PEP 8 compliance via Ruff, type hints required
- **TypeScript**: ESLint + Prettier, functional components, type safety
- Modular design: models/services/api separation (backend), components/lib (frontend)

### Principle V: Specification-First Workflow ✅ PASS
- Spec created before planning
- User stories prioritized (P1, P2, P3)
- Tasks will reference spec in `tasks.md`

### Principle VI: RESTful API Standard ✅ PASS
- REST endpoints: GET, POST, PUT, PATCH, DELETE
- HTTP status codes: 200, 201, 400, 401, 403, 404, 500
- API contract defined in OpenAPI 3.0 format
- Versioned endpoints: `/api/v1/`

### Principle VII: Multi-User Authentication & Authorization ✅ PASS
- Better Auth with JWT tokens
- Backend validates JWT with shared `BETTER_AUTH_SECRET`
- All API endpoints require authentication (except /auth/register and /auth/login)
- Data scoped to `user_id`, authorization checks on all operations

**Constitution Check Result**: ✅ ALL PRINCIPLES SATISFIED

---

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-fullstack-todo/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 technology research
├── data-model.md        # SQLModel schemas and database design
├── quickstart.md        # Local development setup guide
├── contracts/
│   └── api-spec.yaml    # OpenAPI 3.0 REST API contract
├── checklists/
│   └── requirements.md  # Specification quality validation
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Monorepo Structure (Constitution Principle III)
/
├── backend/             # FastAPI workspace
│   ├── src/
│   │   ├── models/      # SQLModel classes
│   │   │   ├── __init__.py
│   │   │   ├── user.py  # User entity
│   │   │   └── task.py  # Task entity
│   │   ├── services/    # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     # Authentication logic
│   │   │   └── task_service.py     # Task CRUD logic
│   │   ├── api/         # FastAPI endpoints
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py     # Auth dependencies
│   │   │   ├── auth.py  # /auth/register, /auth/login
│   │   │   └── tasks.py # /users/{user_id}/tasks endpoints
│   │   ├── auth/        # JWT verification
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py   # JWT encode/decode
│   │   │   └── password.py  # Password hashing
│   │   ├── core/        # Configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py    # Settings (Pydantic BaseSettings)
│   │   │   └── database.py  # SQLModel engine and session
│   │   └── main.py      # FastAPI app entry point
│   ├── alembic/
│   │   ├── versions/    # Database migrations
│   │   └── env.py
│   ├── tests/
│   │   ├── contract/    # API contract tests (OpenAPI compliance)
│   │   ├── integration/ # API endpoint integration tests
│   │   └── unit/        # Model and service unit tests
│   ├── pyproject.toml
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── frontend/            # Next.js workspace
│   ├── src/
│   │   ├── app/         # Next.js App Router
│   │   │   ├── (auth)/  # Auth route group
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── register/
│   │   │   │       └── page.tsx
│   │   │   ├── tasks/   # Protected routes
│   │   │   │   ├── page.tsx         # Task list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx     # Task detail
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/  # React components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── AuthForm.tsx
│   │   └── lib/         # Utilities, API clients
│   │       ├── api/
│   │       │   ├── client.ts        # API client with auth
│   │       │   └── tasks.ts         # Task API functions
│   │       ├── auth/
│   │       │   └── better-auth.ts   # Better Auth config
│   │       └── types.ts             # TypeScript types
│   ├── tests/
│   │   ├── components/  # Component tests
│   │   └── e2e/         # Playwright E2E tests
│   ├── package.json
│   ├── .env.example
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── README.md
│
├── legacy_phase1/       # Phase 1 CLI code (reference only)
│
├── docker-compose.yml   # Local development orchestration
├── .gitignore
└── README.md
```

**Structure Decision**: Monorepo with workspace-based separation enables atomic commits across full stack while maintaining independent deployment capabilities. Docker Compose provides consistent development environment across team members.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All complexity is justified by requirements:

| Potential Concern | Justification | Simpler Alternative Rejected |
|-------------------|---------------|------------------------------|
| Monorepo vs separate repos | Constitution Principle III mandate | Separate repos would complicate API contract sync |
| Docker Compose for local dev | Consistent environments, turnkey setup | Native installs cause "works on my machine" issues |
| JWT auth vs sessions | Stateless, horizontally scalable | Session-based requires Redis, adds stateful dependency |
| SQLModel vs raw SQLAlchemy | Type safety, Pydantic integration | Raw SQLAlchemy requires more boilerplate |

---

## Phase 0: Research (COMPLETE)

**Status**: ✅ Complete - See [research.md](research.md)

**Key Decisions Made**:

1. **Monorepo Structure**: Workspace-based with `/frontend` and `/backend` at root
2. **Authentication**: Better Auth (frontend) + JWT validation (backend) with shared secret
3. **Database Schema**: SQLModel with indexed `user_id` foreign key
4. **API Design**: REST with `/api/v1/users/{user_id}/tasks` for explicit authorization
5. **Local Development**: Docker Compose with PostgreSQL 16, FastAPI, Next.js
6. **API Calls**: Next.js Server Actions for secure token handling

All research complete. Ready for Phase 1 design artifacts.

---

## Phase 1: Design & Contracts (COMPLETE)

**Status**: ✅ Complete - All artifacts generated

### Data Model ✅
**File**: [data-model.md](data-model.md)

**Entities Defined**:
1. **User Entity**:
   - Fields: `id` (PK), `email` (unique, indexed), `hashed_password`, `created_at`
   - Relationships: One-to-many with Task (cascade delete)
   - Validation: Email format, min 8-char password

2. **Task Entity**:
   - Fields: `id` (PK), `title` (max 200), `description` (max 2000), `is_complete`, `created_at`, `updated_at`, `user_id` (FK, indexed)
   - Relationships: Many-to-one with User
   - Indexes: Primary key, `user_id`, composite `(user_id, created_at)`

**Migration Strategy**: Alembic with initial migration creating both tables

### API Contracts ✅
**File**: [contracts/api-spec.yaml](contracts/api-spec.yaml)

**Endpoints Defined** (OpenAPI 3.0):

**Authentication**:
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

**Tasks** (all require JWT authentication):
- `GET /api/v1/users/{user_id}/tasks` - List tasks
- `POST /api/v1/users/{user_id}/tasks` - Create task
- `GET /api/v1/users/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete` - Toggle completion

**Security**: Bearer JWT auth, 401/403 error handling

### Quickstart Guide ✅
**File**: [quickstart.md](quickstart.md)

**Covers**:
- Docker Compose setup (recommended path)
- Local development without Docker
- Database migration commands
- Common troubleshooting scenarios
- Environment variable reference

---

## Re-Evaluation: Constitution Check (Post-Design)

**Gate: Re-check after Phase 1 design complete**

### Design Artifact Compliance

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Spec-Driven Development | ✅ PASS | All design artifacts trace to spec requirements |
| II. Neon PostgreSQL + SQLModel | ✅ PASS | data-model.md defines complete SQLModel schema |
| III. Monorepo Architecture | ✅ PASS | Project structure shows `/frontend` and `/backend` |
| IV. Code Quality Standards | ✅ PASS | Structure enforces modular design (models/services/api) |
| V. Specification-First | ✅ PASS | Design follows from completed spec.md |
| VI. RESTful API Standard | ✅ PASS | OpenAPI contract defines all REST endpoints |
| VII. Multi-User Auth | ✅ PASS | JWT auth in contract, `user_id` scoping in data model |

**Post-Design Result**: ✅ ALL PRINCIPLES SATISFIED

**Ready for `/sp.tasks` command** to generate implementation tasks.

---

## Implementation Strategy

### MVP Approach (P1 User Stories First)

**Phase 1 MVP** (User Stories P1):
1. User Registration and Login (US1)
2. Create and View Tasks (US2)

**Delivers**: Working authentication + basic task management (can demo end-to-end)

**Phase 2 Enhancement** (User Stories P2):
3. Mark Tasks Complete/Incomplete (US3)
4. Edit Tasks (US4)

**Delivers**: Full task lifecycle management

**Phase 3 Polish** (User Stories P3):
5. Delete Tasks (US5)

**Delivers**: Complete feature set per spec

### Parallel Development Opportunities

**After Foundation Complete**:
- Frontend and backend teams can work in parallel
- Backend implements API endpoints per OpenAPI contract
- Frontend consumes contract before backend completion (mock API)

**Example Parallel Workflow**:
1. Backend team implements `/auth/register` and `/auth/login`
2. Frontend team builds registration/login forms (can use mock API initially)
3. Teams integrate when backend endpoints ready
4. Repeat for task endpoints

---

## Risk Analysis

### Top 3 Risks

1. **Risk**: JWT secret leakage
   - **Impact**: HIGH - Compromised secret allows token forgery
   - **Mitigation**: Store in environment variables, never commit, rotate in production
   - **Kill Switch**: Immediate secret rotation invalidates all tokens

2. **Risk**: Cross-user data access bug
   - **Impact**: HIGH - Privacy violation, regulatory risk
   - **Mitigation**: Index on `user_id`, explicit authorization checks on every endpoint
   - **Guardrail**: Integration tests verifying 403 errors for unauthorized access

3. **Risk**: Database connection pool exhaustion
   - **Impact**: MEDIUM - API becomes unresponsive under load
   - **Mitigation**: Configure connection pool limits (max 30), connection pre-ping
   - **Kill Switch**: Auto-scaling backend instances, connection pool monitoring alerts

---

## Testing Strategy

### Backend Tests

**Contract Tests** (`tests/contract/`):
- Validate API responses match OpenAPI schema
- Use `pytest` + `schemathesis` for automated contract testing

**Integration Tests** (`tests/integration/`):
- Test full API workflows (register → login → create task → complete task → delete task)
- Use `httpx` async client with pytest fixtures
- Test authorization failures (403 for wrong user_id, 401 for missing token)

**Unit Tests** (`tests/unit/`):
- Test SQLModel classes (validation, relationships)
- Test service layer logic (password hashing, JWT encode/decode)
- Mock database with pytest fixtures

### Frontend Tests

**Component Tests** (`tests/components/`):
- Test React components in isolation
- Use Jest + React Testing Library
- Mock API calls with MSW (Mock Service Worker)

**E2E Tests** (`tests/e2e/`):
- Test complete user journeys with Playwright
- Scenarios: registration → login → create task → mark complete → logout

---

## Deployment Architecture (Out of Scope for Planning, Noted)

**Frontend**: Vercel or Netlify (edge deployment)
**Backend**: Docker container on AWS ECS / Google Cloud Run
**Database**: Neon Serverless PostgreSQL (managed)
**Secrets**: AWS Secrets Manager / GCP Secret Manager

---

## Open Questions for `/sp.tasks`

1. Should we implement optimistic UI updates for task completion toggle?
2. Do we need rate limiting on authentication endpoints to prevent brute force?
3. Should we add database indices on `created_at` for performance?
4. Do we need Alembic auto-generation or manual migrations?

**Decision**: Defer to task implementation phase. MVP can proceed without these optimizations.

---

## Success Criteria Traceability

| Success Criterion | Implementation Approach |
|-------------------|-------------------------|
| SC-001: Registration in < 1 minute | Simple form, async registration API |
| SC-002: Create task in < 15 seconds | One-click "Add Task" button, inline form |
| SC-003: Task list loads in < 2 seconds | Indexed `user_id` query, limit 100 tasks initially |
| SC-004: Single-click completion toggle | PATCH endpoint with boolean payload |
| SC-005: 100 concurrent users | Stateless JWT, connection pooling, horizontal scaling |
| SC-006: 95% API success rate | Error handling, database retries, health checks |
| SC-007: Zero cross-user data access | Authorization checks on every endpoint, integration tests |
| SC-008: Complete core workflows without assistance | Intuitive UI, clear error messages |
| SC-009: 99% uptime | Neon managed database, auto-scaling backend |
| SC-010: 7-day session persistence | JWT expiration configured to 10080 minutes |

---

## Next Command

**Ready for**: `/sp.tasks` to generate implementation tasks organized by user story

**Expected Output**: `tasks.md` with:
- Setup phase (project initialization)
- Foundational phase (database, auth infrastructure)
- User Story 1 tasks (registration + login)
- User Story 2 tasks (create + view tasks)
- User Story 3 tasks (mark complete)
- User Story 4 tasks (edit tasks)
- User Story 5 tasks (delete tasks)
- Polish phase (testing, deployment)

**Branch**: `002-phase2-fullstack-todo`
**Plan**: `specs/002-phase2-fullstack-todo/plan.md` (this file)
