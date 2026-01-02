# Tasks: Phase 1 In-Memory Todo CLI

**Input**: Design documents from `/specs/001-phase1-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/
**Status**: ALL TASKS COMPLETED

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize Python 3.13+ project with pyproject.toml
- [X] T002 [P] Configure pytest in pyproject.toml
- [X] T003 [P] Create src/ directory structure (models/, services/, cli/)
- [X] T004 [P] Create tests/ directory structure (unit/, integration/)
- [X] T005 Create .gitignore for Python project

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create Task model in src/models/task.py with dataclass and validation
- [X] T007 Create TaskService in src/services/task_service.py with in-memory storage and ID counter
- [X] T008 [P] Implement add_task method in TaskService (FR-001, FR-002, FR-010, FR-011)
- [X] T009 [P] Implement get_all_tasks method in TaskService (FR-004)
- [X] T010 [P] Implement get_task_by_id method in TaskService (FR-008)
- [X] T011 [P] Implement update_task method in TaskService (FR-006)
- [X] T012 [P] Implement mark_complete method in TaskService (FR-005)
- [X] T013 [P] Implement delete_task method in TaskService (FR-007)
- [X] T014 Create unit tests for Task model in tests/unit/test_task.py
- [X] T015 Create unit tests for TaskService in tests/unit/test_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) MVP

**Goal**: Users can create new tasks with a title (required) and description (optional)

**Independent Test**: Can be tested by launching the app, selecting "Add Task", entering a title, and verifying the task appears in the task list.

**Related FR**: FR-001, FR-002, FR-010, FR-011, FR-012

### Implementation for User Story 1

- [X] T016 [US1] Create input handlers for Add Task flow in src/cli/menu.py
- [X] T017 [US1] Implement handle_add_task method in src/cli/menu.py (FR-001, FR-012)
- [X] T018 [US1] Add Add Task to main menu in src/cli/menu.py
- [X] T019 [US1] Connect Add Task menu option to TaskService in src/main.py

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Users can see all tasks with their ID, title, status, and description

**Independent Test**: Can be tested by launching the app, selecting "View Tasks", and verifying all previously added tasks are displayed.

**Related FR**: FR-004

### Implementation for User Story 2

- [X] T020 [US2] Create input handlers for View Tasks flow in src/cli/menu.py
- [X] T021 [US2] Implement handle_view_tasks method in src/cli/menu.py (FR-004)
- [X] T022 [US2] Add View Tasks menu option to main menu in src/cli/menu.py
- [X] T023 [US2] Connect View Tasks menu option to TaskService in src/main.py

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P1)

**Goal**: Users can toggle a task's status from Pending to Completed

**Independent Test**: Can be tested by adding a task, viewing it as "Pending", marking it complete, and verifying the status changes.

**Related FR**: FR-005, FR-008

### Implementation for User Story 3

- [X] T024 [US3] Create input handlers for Mark Complete flow in src/cli/menu.py
- [X] T025 [US3] Implement handle_mark_complete method in src/cli/menu.py (FR-005, FR-008)
- [X] T026 [US3] Add Mark Complete menu option to main menu in src/cli/menu.py
- [X] T027 [US3] Connect Mark Complete menu option to TaskService in src/main.py

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can modify a task's title or description using its ID

**Independent Test**: Can be tested by adding a task, viewing it, updating the title or description, and verifying the changes.

**Related FR**: FR-006, FR-008

### Implementation for User Story 4

- [X] T028 [US4] Create input handlers for Update Task flow in src/cli/menu.py
- [X] T029 [US4] Implement handle_update_task method in src/cli/menu.py (FR-006, FR-008)
- [X] T030 [US4] Add Update Task menu option to main menu in src/cli/menu.py
- [X] T031 [US4] Connect Update Task menu option to TaskService in src/main.py

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Users can permanently remove a task using its ID

**Independent Test**: Can be tested by adding a task, deleting it, and verifying it no longer appears.

**Related FR**: FR-007, FR-008

### Implementation for User Story 5

- [X] T032 [US5] Create input handlers for Delete Task flow in src/cli/menu.py
- [X] T033 [US5] Implement handle_delete_task method in src/cli/menu.py (FR-007, FR-008)
- [X] T034 [US5] Add Delete Task menu option to main menu in src/cli/menu.py
- [X] T035 [US5] Connect Delete Task menu option to TaskService in src/main.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T036 Create integration tests for CLI workflows in tests/integration/test_cli.py
- [X] T037 [P] Add main menu loop and Exit option in src/main.py
- [X] T038 [P] Add input validation helper functions in src/cli/menu.py
- [X] T039 [P] Add error message formatting in src/cli/menu.py
- [X] T040 [P] Add logging for user operations in src/cli/menu.py (optional per constitution)
- [X] T041 Run quickstart.md validation - verify app starts and completes basic workflow
- [X] T042 [P] PEP 8 compliance check using ruff or flake8
- [X] T043 [P] Fix any linting issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) or sequentially
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- CLI handlers before menu connections
- Service methods before CLI handlers
- Model before Service
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational is done, all user stories can start in parallel (if team capacity allows)
- All polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
Task: "Create input handlers for Add Task flow in src/cli/menu.py"
Task: "Implement handle_add_task method in src/cli/menu.py"
Task: "Add Add Task to main menu in src/cli/menu.py"
Task: "Connect Add Task menu option to TaskService in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test Add Task independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Complete Phase 8: Polish

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Summary

- **Total Tasks**: 43
- **Completed Tasks**: 43 (100%)
- **Setup Phase**: 5 tasks
- **Foundational Phase**: 10 tasks (blocks all user stories)
- **User Story 1 (P1)**: 4 tasks
- **User Story 2 (P1)**: 4 tasks
- **User Story 3 (P1)**: 4 tasks
- **User Story 4 (P2)**: 4 tasks
- **User Story 5 (P2)**: 4 tasks
- **Polish Phase**: 8 tasks

### Test Results

- **Unit Tests**: 38 passed (test_task.py, test_service.py)
- **Integration Tests**: 14 passed (test_cli.py)
- **Total**: 52 tests passed
- **PEP 8 Compliance**: All checks passed (ruff)

### Independent Test Criteria

- **US1**: Launch app → Add Task → View Tasks → Task appears with "Pending" status
- **US2**: Launch app → View Tasks → Empty state or tasks displayed with correct columns
- **US3**: Add Task → Mark Complete → View Tasks → Status shows "Completed"
- **US4**: Add Task → Update Task (change title) → View Tasks → Title updated
- **US5**: Add Task → Delete Task → View Tasks → Task no longer appears

### Parallel Opportunities

- Setup tasks T001-T005 can run in parallel
- Foundational tasks T006-T015 can run in parallel
- All user story phases (3-7) are independent and can run in parallel
- Polish tasks T036-T043 can run in parallel

### Suggested MVP Scope

Complete Phases 1, 2, and 3 (User Story 1: Add New Task) for minimum viable product.
