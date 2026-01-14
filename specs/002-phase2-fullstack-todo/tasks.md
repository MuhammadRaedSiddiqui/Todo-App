---
description: "Implementation tasks for Phase 2 Full-Stack Todo App"
---

# Tasks: Phase 2 Full-Stack Todo App

**Input**: Design documents from `/specs/002-phase2-fullstack-todo/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/api-spec.yaml, research.md

**Tests**: Tests are NOT explicitly requested in specification - focusing on implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo (Todo App)**: `backend/src/`, `frontend/src/` (CONSTITUTION MANDATE: Next.js 16+ frontend, FastAPI backend, Neon PostgreSQL, Better Auth)
- Backend paths: `backend/src/models/`, `backend/src/services/`, `backend/src/api/`, `backend/src/auth/`
- Frontend paths: `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure per ADR-001

- [ ] T001 Create docker-compose.yml in repository root with postgres, backend, and frontend services per quickstart.md
- [ ] T002 Create backend/Dockerfile with Python 3.13-slim, UV installation, and uvicorn command
- [ ] T003 Create frontend/Dockerfile with Node 20-alpine, npm ci, and next dev command
- [ ] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
- [ ] T005 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [ ] T006 [P] Update backend/pyproject.toml with FastAPI 0.115+, SQLModel 0.0.22+, psycopg2-binary, python-jose, passlib, alembic dependencies
- [ ] T007 [P] Update frontend/package.json with better-auth 1.0+ dependency
- [ ] T008 [P] Create frontend/tailwind.config.js per plan.md structure
- [ ] T009 [P] Create frontend/next.config.js with reactStrictMode enabled

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Create backend/src/core/config.py with Pydantic BaseSettings for DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES (FR-006)
- [ ] T011 Create backend/src/core/database.py with SQLModel engine creation using DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True per ADR-003
- [ ] T012 Add get_session() dependency function in backend/src/core/database.py for FastAPI dependency injection
- [ ] T013 Create backend/alembic/env.py to configure Alembic with SQLModel metadata per data-model.md migration strategy
- [ ] T014 Create backend/alembic.ini with script_location and sqlalchemy.url configuration
- [ ] T015 Generate initial Alembic migration in backend/alembic/versions/001_initial_schema.py creating users and tasks tables per data-model.md
- [ ] T016 Create backend/src/models/__init__.py importing User and Task models
- [ ] T017 [P] Create backend/src/models/user.py with User SQLModel class per data-model.md (id, email, hashed_password, created_at, tasks relationship)
- [ ] T018 [P] Create backend/src/models/task.py with Task SQLModel class per data-model.md (id, title, description, is_complete, created_at, updated_at, user_id FK, user relationship)
- [ ] T019 Create backend/src/auth/password.py with bcrypt hash_password() and verify_password() functions using passlib (FR-004)
- [ ] T020 Create backend/src/auth/jwt.py with create_access_token() and verify_token() functions using python-jose, HS256 algorithm, BETTER_AUTH_SECRET per ADR-002
- [ ] T021 Create backend/src/api/dependencies.py with get_current_user() FastAPI dependency that validates JWT token and returns User object (ADR-002 authentication flow)
- [ ] T022 Create backend/src/main.py with FastAPI app initialization, CORS middleware for http://localhost:3000, and root health check endpoint
- [ ] T023 Create frontend/src/lib/auth/better-auth.ts with Better Auth configuration using BETTER_AUTH_SECRET, 7-day session expiration, HTTP-only cookies per ADR-002
- [ ] T024 Create frontend/src/lib/api/client.ts with fetch wrapper that automatically attaches JWT token from cookies to Authorization header
- [ ] T025 Create frontend/src/app/layout.tsx with RootLayout component, metadata (title, description), and globals.css import
- [ ] T026 Create frontend/src/app/globals.css with Tailwind CSS directives (@tailwind base, components, utilities)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Implement authentication system with user registration, login, logout, and session persistence (FR-001 through FR-008)

**Independent Test**: Create new account → login → verify session persists → logout → verify redirect

### Implementation for User Story 1

- [ ] T027 [P] [US1] Create backend/src/services/auth_service.py with register_user() function that validates email format (FR-002), checks min 8-char password (FR-003), hashes password, creates User record (FR-001)
- [ ] T028 [P] [US1] Add authenticate_user() function to backend/src/services/auth_service.py that finds user by email, verifies password hash, returns User or None (FR-005, FR-008)
- [ ] T029 [US1] Create backend/src/api/auth.py APIRouter with POST /api/v1/auth/register endpoint that calls register_user(), generates JWT token, returns AuthResponse per contracts/api-spec.yaml
- [ ] T030 [US1] Add POST /api/v1/auth/login endpoint to backend/src/api/auth.py that calls authenticate_user(), generates JWT token with 7-day expiration (FR-006), returns AuthResponse or 401 error per contracts/api-spec.yaml
- [ ] T031 [US1] Mount auth router in backend/src/main.py at /api/v1 prefix
- [ ] T032 [US1] Create frontend/src/app/(auth)/register/page.tsx with registration form (email, password fields), calls Better Auth register, redirects to /tasks on success
- [ ] T033 [US1] Create frontend/src/app/(auth)/login/page.tsx with login form (email, password fields), calls Better Auth login, redirects to /tasks on success
- [ ] T034 [US1] Create frontend/src/components/AuthForm.tsx reusable component with email/password inputs, submit button, and error display for registration and login pages
- [ ] T035 [US1] Add logout functionality in frontend/src/lib/auth/better-auth.ts that clears HTTP-only cookie and redirects to /login (FR-007)
- [ ] T036 [US1] Create frontend/src/app/page.tsx that redirects authenticated users to /tasks and unauthenticated users to /login

**Checkpoint**: At this point, User Story 1 should be fully functional - users can register, login, and logout independently

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement task creation and listing with user-scoped data access (FR-009 through FR-016, FR-021 through FR-027)

**Independent Test**: Login → create multiple tasks → verify they appear in list → verify user can only see own tasks → view single task detail

### Implementation for User Story 2

- [X] T037 [US2] Create backend/src/services/task_service.py with create_task() function that validates title max 200 chars (FR-010), description max 2000 chars (FR-011), sets user_id, creates Task record (FR-009)
- [X] T038 [US2] Add list_user_tasks() function to backend/src/services/task_service.py that queries tasks filtered by user_id with created_at DESC order (FR-014, FR-015, FR-021)
- [X] T039 [US2] Add get_task_by_id() function to backend/src/services/task_service.py that queries task by id AND user_id to enforce authorization (FR-016, FR-022)
- [X] T040 [US2] Create backend/src/api/tasks.py APIRouter with GET /api/v1/users/{user_id}/tasks endpoint that verifies current_user.id == user_id (403 if not), calls list_user_tasks(), returns List[Task] per contracts/api-spec.yaml (FR-025, FR-026)
- [X] T041 [US2] Add POST /api/v1/users/{user_id}/tasks endpoint to backend/src/api/tasks.py that verifies user_id authorization, calls create_task(), returns 201 with Task per contracts/api-spec.yaml
- [X] T042 [US2] Add GET /api/v1/users/{user_id}/tasks/{task_id} endpoint to backend/src/api/tasks.py that verifies user_id authorization, calls get_task_by_id(), returns Task or 404 per contracts/api-spec.yaml
- [X] T043 [US2] Mount tasks router in backend/src/main.py at /api/v1 prefix
- [X] T044 [US2] Create frontend/src/lib/api/tasks.ts with listTasks(user_id) async function using API client with JWT token
- [X] T045 [US2] Add createTask(user_id, title, description) async function to frontend/src/lib/api/tasks.ts
- [X] T046 [US2] Add getTask(user_id, task_id) async function to frontend/src/lib/api/tasks.ts
- [X] T047 [US2] Create frontend/src/lib/types.ts with Task, User, and AuthResponse TypeScript interfaces matching API contracts
- [X] T048 [US2] Create frontend/src/app/tasks/page.tsx that fetches tasks via listTasks(), displays TaskList component, includes "Add Task" button
- [X] T049 [US2] Create frontend/src/components/TaskList.tsx that renders list of TaskItem components or "No tasks yet. Create your first task!" message when empty
- [X] T050 [US2] Create frontend/src/components/TaskItem.tsx that displays task title, description preview, created date, and completion status (read-only for now)
- [X] T051 [US2] Create frontend/src/components/TaskForm.tsx with title input (required, max 200), description textarea (optional, max 2000), submit/cancel buttons, calls createTask() on submit
- [X] T052 [US2] Add TaskForm modal/drawer to frontend/src/app/tasks/page.tsx triggered by "Add Task" button
- [X] T053 [US2] Create frontend/src/app/tasks/[id]/page.tsx that fetches single task via getTask(), displays full task details (title, description, status, dates)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - basic todo app MVP is functional

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Implement task completion toggle with visual indicators (FR-017, FR-018)

**Independent Test**: Login → create task → mark complete (verify visual change) → mark incomplete (verify visual change) → verify persistence

### Implementation for User Story 3

- [X] T054 [US3] Add toggle_task_complete() function to backend/src/services/task_service.py that finds task by id AND user_id, updates is_complete field, updates updated_at timestamp (FR-017, FR-018)
- [X] T055 [US3] Create PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete endpoint in backend/src/api/tasks.py that verifies user_id authorization, calls toggle_task_complete(), returns updated Task per contracts/api-spec.yaml
- [X] T056 [US3] Add toggleTaskComplete(user_id, task_id, is_complete) async function to frontend/src/lib/api/tasks.ts
- [X] T057 [US3] Update frontend/src/components/TaskItem.tsx to add checkbox that calls toggleTaskComplete() on click
- [X] T058 [US3] Add visual styling to frontend/src/components/TaskItem.tsx for completed tasks (strikethrough title, checkmark icon, or different text color)
- [X] T059 [US3] Implement optimistic UI update in frontend/src/components/TaskItem.tsx that immediately reflects completion state change before API response

**Checkpoint**: Task completion tracking is now functional independently

---

## Phase 6: User Story 4 - Edit Tasks (Priority: P2)

**Goal**: Implement task editing with title and description updates (FR-019, FR-023)

**Independent Test**: Login → create task → edit title → edit description → verify changes persist → test validation (empty title error)

### Implementation for User Story 4

- [X] T060 [US4] Add update_task() function to backend/src/services/task_service.py that finds task by id AND user_id, validates title required and max 200 chars, description max 2000 chars, updates fields, updates updated_at timestamp (FR-019)
- [X] T061 [US4] Create PUT /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/src/api/tasks.py that verifies user_id authorization (FR-023), calls update_task(), returns updated Task or 400/403/404 per contracts/api-spec.yaml
- [X] T062 [US4] Add updateTask(user_id, task_id, title, description) async function to frontend/src/lib/api/tasks.ts
- [X] T063 [US4] Create edit mode in frontend/src/components/TaskItem.tsx or frontend/src/app/tasks/[id]/page.tsx with inline editing or modal
- [X] T064 [US4] Reuse or extend frontend/src/components/TaskForm.tsx for edit mode with pre-filled values, validation (title required), cancel discards changes
- [X] T065 [US4] Add "Edit" button to TaskItem component that triggers edit mode
- [X] T066 [US4] Implement validation error display in TaskForm when title is empty on save attempt

**Checkpoint**: Task editing is now functional independently

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Implement permanent task deletion with confirmation (FR-020, FR-024)

**Independent Test**: Login → create task → delete with cancel (verify not deleted) → delete with confirm (verify removed and not in list) → refresh page (verify still removed)

### Implementation for User Story 5

- [X] T067 [US5] Add delete_task() function to backend/src/services/task_service.py that finds task by id AND user_id, deletes Task record (FR-020)
- [X] T068 [US5] Create DELETE /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/src/api/tasks.py that verifies user_id authorization (FR-024), calls delete_task(), returns 204 or 403/404 per contracts/api-spec.yaml
- [X] T069 [US5] Add deleteTask(user_id, task_id) async function to frontend/src/lib/api/tasks.ts
- [X] T070 [US5] Add "Delete" button to frontend/src/components/TaskItem.tsx that triggers confirmation dialog
- [X] T071 [US5] Implement confirmation dialog component in frontend showing "Are you sure?" message with Cancel/Delete buttons
- [X] T072 [US5] Call deleteTask() on confirm, remove task from UI, redirect to /tasks if on detail page

**Checkpoint**: All user stories (P1, P2, P3) are now independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T073 [P] Add loading states to all frontend API calls (spinner or skeleton UI during fetch)
- [X] T074 [P] Add error boundary component in frontend/src/app/error.tsx to catch and display runtime errors gracefully
- [X] T075 [P] Add toast notifications in frontend for successful actions (task created, updated, deleted) and errors
- [X] T076 [P] Implement input validation feedback in frontend forms (real-time character count for title/description max lengths)
- [X] T077 [P] Add backend error handling middleware in backend/src/main.py to catch unhandled exceptions and return 500 with proper error format
- [X] T078 [P] Add backend request logging middleware in backend/src/main.py to log all API requests with timestamp, method, path, status code
- [X] T079 [P] Update frontend/src/app/page.tsx with proper landing page or dashboard instead of just redirect
- [X] T080 [P] Add "Logout" button to frontend navigation/header that calls Better Auth logout
- [X] T081 [P] Implement protected route wrapper in frontend that redirects to /login if user not authenticated
- [ ] T082 Verify quickstart.md instructions by running `docker compose up` and testing full user workflow
- [ ] T083 Run Alembic upgrade head to apply database migrations
- [X] T084 [P] Run backend linter: `cd backend && ruff check src` and fix any PEP 8 violations
- [X] T085 [P] Run frontend linter: `cd frontend && npm run lint` and fix any ESLint errors
- [X] T086 [P] Run frontend type check: `cd frontend && npm run type-check` and fix any TypeScript errors
- [X] T087 Update README.md with updated project status, Phase 2 architecture overview, and quickstart link

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1 - Auth): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P1 - Create/View Tasks): Can start after Foundational (Phase 2) - Requires US1 for authentication context but independently testable with mock auth
  - User Story 3 (P2 - Mark Complete): Can start after Foundational (Phase 2) - Requires US2 tasks to exist but independently testable
  - User Story 4 (P2 - Edit Tasks): Can start after Foundational (Phase 2) - Requires US2 tasks to exist but independently testable
  - User Story 5 (P3 - Delete Tasks): Can start after Foundational (Phase 2) - Requires US2 tasks to exist but independently testable
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Auth)**: Can start after Foundational (Phase 2) - **No dependencies on other stories**
- **User Story 2 (P1 - Tasks)**: Can start after Foundational (Phase 2) - **Requires US1 complete for authentication, but can be developed in parallel with mock auth**
- **User Story 3 (P2 - Complete)**: Can start after Foundational (Phase 2) - **Requires US2 for tasks to exist, but independently testable**
- **User Story 4 (P2 - Edit)**: Can start after Foundational (Phase 2) - **Requires US2 for tasks to exist, but independently testable**
- **User Story 5 (P3 - Delete)**: Can start after Foundational (Phase 2) - **Requires US2 for tasks to exist, but independently testable**

### Within Each User Story

- Backend services before API endpoints
- API endpoints before frontend API client functions
- Frontend API client before UI components
- Core components before composite pages

### Parallel Opportunities

- **Setup Phase**: Tasks T002-T009 (all marked [P]) can run in parallel (different files)
- **Foundational Phase**: Tasks T017-T018 (models), T023-T026 (frontend config) can run in parallel
- **Within Each User Story**: Tasks marked [P] within the same story can run in parallel
- **Across User Stories**: After Foundational complete, multiple user stories can be worked on in parallel by different developers (US1, US2, US3, US4, US5 are independently testable)
- **Polish Phase**: Most tasks marked [P] can run in parallel (different concerns)

---

## Parallel Example: Foundational Phase

```bash
# Launch backend models in parallel:
Task T017: "Create backend/src/models/user.py"
Task T018: "Create backend/src/models/task.py"

# Launch frontend config in parallel:
Task T023: "Create frontend/src/lib/auth/better-auth.ts"
Task T024: "Create frontend/src/lib/api/client.ts"
Task T025: "Create frontend/src/app/layout.tsx"
Task T026: "Create frontend/src/app/globals.css"
```

---

## Implementation Strategy

### MVP First (User Stories P1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Create/View Tasks)
5. **STOP and VALIDATE**: Test complete user workflow (register → login → create task → view task → logout)
6. Deploy/demo if ready - **This is the minimum viable product**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently → Deploy/Demo
3. Add User Story 2 (Tasks) → Test independently → Deploy/Demo (**MVP milestone**)
4. Add User Story 3 (Complete) → Test independently → Deploy/Demo
5. Add User Story 4 (Edit) → Test independently → Deploy/Demo
6. Add User Story 5 (Delete) → Test independently → Deploy/Demo
7. Add Polish Phase → Final release
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers after Foundational phase complete:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: User Story 1 (Authentication) - T027 through T036
   - **Developer B**: User Story 2 (Tasks) - T037 through T053 (can use mock auth initially)
   - **Developer C**: User Story 3 (Complete) - T054 through T059 (integrate after US2 complete)
3. Stories complete and integrate independently

---

## Notes

- All tasks reference ADR decisions: ADR-001 (Monorepo), ADR-002 (Auth), ADR-003 (Database)
- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability to spec.md
- Each user story should be independently completable and testable
- Commit after each task or logical group with reference to Task ID (e.g., `[T027] Implement user registration service`)
- Stop at any checkpoint to validate story independently before proceeding
- **Critical Security**: Every API endpoint MUST verify user_id matches authenticated user (FR-025 through FR-027)
- **Performance**: All task queries MUST filter by user_id to use index (ADR-003, data-model.md)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Total Tasks**: 87
- **Setup Phase**: 9 tasks
- **Foundational Phase**: 17 tasks (BLOCKING)
- **User Story 1 (P1 - Auth)**: 10 tasks
- **User Story 2 (P1 - Tasks)**: 17 tasks
- **User Story 3 (P2 - Complete)**: 6 tasks
- **User Story 4 (P2 - Edit)**: 7 tasks
- **User Story 5 (P3 - Delete)**: 6 tasks
- **Polish Phase**: 15 tasks

**MVP Scope** (P1 stories only): 53 tasks (Setup + Foundational + US1 + US2)

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phases
