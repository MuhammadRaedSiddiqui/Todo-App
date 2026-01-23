---

description: "Task list for AI Chatbot implementation"
---

# Tasks: AI Chatbot for Todo Management

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Tests are OPTIONAL - not included in this task list as they were not explicitly requested in the specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo (Todo App)**: `backend/src/`, `frontend/src/` (CONSTITUTION MANDATE: Next.js 16+ frontend, FastAPI backend, Neon PostgreSQL, Better Auth)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install OpenAI Python SDK in backend/pyproject.toml
- [x] T002 [P] Install Vercel AI SDK in frontend/package.json
- [x] T003 [P] Add GROQ_API_KEY to backend/.env.example
- [x] T004 [P] Add GROQ_MODEL constant to backend/.env.example
- [x] T005 [P] Add GROQ_BASE_URL to backend/.env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Conversation SQLModel in backend/src/models/conversation.py
- [x] T007 [P] Create Message SQLModel in backend/src/models/message.py
- [x] T008 Create database migration for conversations and messages tables in backend/migrations/versions/003_create_chat_tables.py
- [x] T009 Run database migration to create conversations and messages tables
- [x] T010 [P] Create Groq client wrapper in backend/src/services/groq_client.py
- [x] T011 [P] Create tool registry for MCP tool schemas in backend/src/tools/tool_registry.py
- [x] T012 [P] Create tool executor service in backend/src/services/tool_executor.py
- [x] T013 Verify Groq connection with test script in backend/test_groq.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, read, update, and delete tasks using natural language commands

**Independent Test**: Send chat messages requesting task operations and verify tasks are correctly created/updated/deleted in database

### Implementation for User Story 1

- [x] T014 [P] [US1] Define add_task tool schema in backend/src/tools/task_tools.py
- [x] T015 [P] [US1] Define list_tasks tool schema in backend/src/tools/task_tools.py
- [x] T016 [P] [US1] Define update_task tool schema in backend/src/tools/task_tools.py
- [x] T017 [P] [US1] Define delete_task tool schema in backend/src/tools/task_tools.py
- [x] T018 [P] [US1] Define get_task tool schema in backend/src/tools/task_tools.py
- [x] T019 [US1] Implement add_task tool execution function in backend/src/tools/task_tools.py
- [x] T020 [US1] Implement list_tasks tool execution function in backend/src/tools/task_tools.py
- [x] T021 [US1] Implement update_task tool execution function in backend/src/tools/task_tools.py
- [x] T022 [US1] Implement delete_task tool execution function in backend/src/tools/task_tools.py
- [x] T023 [US1] Implement get_task tool execution function in backend/src/tools/task_tools.py
- [x] T024 [US1] Register all tool schemas in tool registry in backend/src/tools/tool_registry.py
- [x] T025 [US1] Implement chat service orchestration logic in backend/src/services/chat_service.py
- [x] T026 [US1] Implement POST /api/chat/message endpoint in backend/src/api/chat.py
- [x] T027 [US1] Implement GET /api/chat/conversations endpoint in backend/src/api/conversations.py
- [x] T028 [US1] Implement GET /api/chat/conversations/{id} endpoint in backend/src/api/conversations.py
- [x] T029 [US1] Implement DELETE /api/chat/conversations/{id} endpoint in backend/src/api/conversations.py
- [x] T030 [US1] Add JWT authentication middleware to chat endpoints in backend/src/api/chat.py
- [x] T031 [US1] Add user_id scoping to all conversation queries in backend/src/api/conversations.py
- [x] T032 [P] [US1] Create TypeScript types for chat messages in frontend/src/lib/types.ts
- [x] T033 [P] [US1] Create chat API client in frontend/src/lib/chat-client.ts
- [x] T034 [US1] Create ChatInterface component with useChat hook in frontend/src/components/chat/ChatInterface.tsx
- [x] T035 [US1] Create MessageList component in frontend/src/components/chat/MessageList.tsx
- [x] T036 [US1] Create MessageInput component in frontend/src/components/chat/MessageInput.tsx
- [x] T037 [US1] Create ToolCallDisplay component in frontend/src/components/chat/ToolCallDisplay.tsx
- [x] T038 [US1] Create chat page in frontend/src/app/chat/page.tsx
- [x] T039 [US1] Add error handling for Groq API failures in backend/src/services/chat_service.py
- [x] T040 [US1] Add rate limiting handling for Groq free tier in backend/src/services/groq_client.py
- [x] T041 [US1] Add input sanitization to prevent prompt injection in backend/src/services/chat_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversational Context Awareness (Priority: P2)

**Goal**: Enable multi-turn conversations where users can reference previous messages using pronouns

**Independent Test**: Conduct multi-turn conversations with pronoun references and verify correct interpretation

### Implementation for User Story 2

- [x] T042 [US2] Implement conversation history retrieval in backend/src/services/chat_service.py
- [x] T043 [US2] Implement context window management (truncate old messages) in backend/src/services/chat_service.py
- [x] T044 [US2] Add conversation_id parameter handling to POST /api/chat/message in backend/src/api/chat.py
- [x] T045 [US2] Implement conversation state tracking in ChatInterface component in frontend/src/components/chat/ChatInterface.tsx
- [x] T046 [US2] Add conversation history display to MessageList component in frontend/src/components/chat/MessageList.tsx
- [x] T047 [US2] Implement new conversation creation flow in frontend/src/components/chat/ChatInterface.tsx
- [x] T048 [US2] Add conversation switching UI in frontend/src/app/chat/page.tsx
- [x] T049 [US2] Implement context-aware message formatting in backend/src/services/chat_service.py
- [x] T050 [US2] Add updated_at timestamp update on new messages in backend/src/models/conversation.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Intelligent Task Suggestions (Priority: P3)

**Goal**: Chatbot proactively suggests task-related actions based on conversation context

**Independent Test**: Create scenarios where suggestions are appropriate and verify chatbot offers recommendations

### Implementation for User Story 3

- [x] T051 [US3] Implement task analysis logic in backend/src/services/chat_service.py
- [x] T052 [US3] Add suggestion generation for overdue tasks in backend/src/services/chat_service.py
- [x] T053 [US3] Add suggestion generation for past due dates in backend/src/services/chat_service.py
- [x] T054 [US3] Add suggestion generation for vague task descriptions in backend/src/services/chat_service.py
- [x] T055 [US3] Implement suggestion formatting in AI system prompt in backend/src/services/groq_client.py
- [x] T056 [US3] Add suggestion display styling in frontend/src/components/chat/MessageList.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T057 [P] Add logging for all AI interactions in backend/src/services/chat_service.py
- [x] T058 [P] Add error logging for tool execution failures in backend/src/services/tool_executor.py
- [x] T059 [P] Implement graceful error messages for users in backend/src/api/chat.py
- [x] T060 [P] Add loading states to ChatInterface in frontend/src/components/chat/ChatInterface.tsx
- [x] T061 [P] Add error display to ChatInterface in frontend/src/components/chat/ChatInterface.tsx
- [x] T062 [P] Optimize database queries with proper indexing in backend/migrations/versions/003_create_chat_tables.py
- [x] T063 [P] Add CORS configuration for frontend in backend/src/main.py
- [x] T064 [P] Add API documentation for chat endpoints in backend/src/api/chat.py
- [x] T065 Validate implementation against quickstart.md instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable

### Within Each User Story

- Tool schemas before tool execution functions
- Tool execution functions before chat service
- Chat service before API endpoints
- Backend endpoints before frontend components
- Core components before page integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tool schema definitions (T014-T018) can run in parallel
- Tool execution implementations (T019-T023) can run in parallel after schemas complete
- Frontend type definitions and API client (T032-T033) can run in parallel
- Frontend components (T035-T037) can run in parallel after ChatInterface is created
- Polish tasks (T057-T064) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tool schemas together:
Task T014: "Define add_task tool schema in backend/src/tools/task_tools.py"
Task T015: "Define list_tasks tool schema in backend/src/tools/task_tools.py"
Task T016: "Define update_task tool schema in backend/src/tools/task_tools.py"
Task T017: "Define delete_task tool schema in backend/src/tools/task_tools.py"
Task T018: "Define get_task tool schema in backend/src/tools/task_tools.py"

# After schemas complete, launch all tool implementations together:
Task T019: "Implement add_task tool execution function"
Task T020: "Implement list_tasks tool execution function"
Task T021: "Implement update_task tool execution function"
Task T022: "Implement delete_task tool execution function"
Task T023: "Implement get_task tool execution function"

# Launch frontend components in parallel:
Task T035: "Create MessageList component"
Task T036: "Create MessageInput component"
Task T037: "Create ToolCallDisplay component"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
