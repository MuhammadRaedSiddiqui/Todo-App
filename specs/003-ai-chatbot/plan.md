# Implementation Plan: AI Chatbot for Todo Management

**Branch**: `003-ai-chatbot` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-powered chatbot interface that enables users to manage their todo tasks using natural language. The system uses Groq's Llama 3.3 model via OpenAI-compatible API, with stateless architecture storing conversation history in PostgreSQL. The chatbot interprets user intent and executes task operations (create, read, update, delete) through a tool calling interface following the Model Context Protocol pattern.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Node.js 20+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Python SDK (configured for Groq), Pydantic
- Frontend: Next.js 16+, React, Vercel AI SDK (useChat hook), Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (Conversation, Message tables)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Vercel deployment for frontend, serverless backend)
**Project Type**: Monorepo (frontend + backend)
**Performance Goals**: <5 seconds response time for 95% of chat requests, <3 seconds for simple queries
**Constraints**:
- Groq free tier rate limits (30 requests/minute)
- ~8K token context window for Llama 3.3
- Stateless design (no in-memory session state)
- Must use OpenAI SDK compatibility pattern (base_url override)
**Scale/Scope**: Multi-user system with per-user conversation isolation, support for 100+ concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I - Spec-Driven Development**: ✅ PASS
- Feature specification created at `specs/003-ai-chatbot/spec.md`
- Implementation plan being created at `specs/003-ai-chatbot/plan.md`
- Tasks will be generated in `specs/003-ai-chatbot/tasks.md`

**Principle II - Persistence Layer with Neon PostgreSQL**: ✅ PASS
- Conversation and Message entities will use SQLModel ORM
- Database schema designed for stateless conversation history storage
- Migrations will be versioned and reversible

**Principle III - Monorepo Architecture**: ✅ PASS
- Backend: FastAPI endpoints in `backend/src/api/chat.py`
- Frontend: Next.js chat interface in `frontend/src/app/chat/`
- Contracts documented in `specs/003-ai-chatbot/contracts/`

**Principle IV - Code Quality Standards**: ✅ PASS
- Python: PEP 8, type hints, modular service layer
- TypeScript: ESLint + Prettier, functional React components

**Principle V - Specification-First Workflow**: ✅ PASS
- Spec completed with 3 prioritized user stories (P1, P2, P3)
- Acceptance criteria and edge cases documented

**Principle VI - RESTful API Standard**: ✅ PASS
- POST /api/chat/message - Send chat message and receive response
- GET /api/chat/conversations - List user's conversations
- GET /api/chat/conversations/{id}/messages - Retrieve conversation history
- DELETE /api/chat/conversations/{id} - Delete conversation

**Principle VII - Multi-User Authentication & Authorization**: ✅ PASS
- JWT token verification on all chat endpoints
- Conversation and Message entities scoped to `user_id`
- Tool execution respects user data boundaries

**Principle VIII - AI Chatbot Integration with Groq**: ✅ PASS
- Using Groq with Llama 3.3 model (`llama-3.3-70b-versatile`)
- OpenAI Python SDK with `base_url="https://api.groq.com/openai/v1"`
- Standard Chat Completions API with Tool Calling (not Assistants API)
- Stateless design with database-backed conversation history
- MCP-style tool definitions for task operations

**Gate Result**: ✅ ALL PRINCIPLES SATISFIED - Proceed to Phase 0

---

## Phase 0: Research (Complete)

**Output**: `research.md`

**Key Decisions**:
1. **Groq Integration**: Use OpenAI Python SDK with `base_url="https://api.groq.com/openai/v1"`
2. **Tool Calling**: OpenAI function calling schema format (MCP pattern)
3. **Frontend**: Vercel AI SDK `useChat` hook (not @openai/chatkit-react)
4. **Database**: Two-table design (Conversation, Message)
5. **Stateless Design**: Retrieve full conversation history on each request

**Alternatives Considered**:
- Custom HTTP client (rejected - unnecessary complexity)
- LangChain integration (rejected - adds abstraction overhead)
- Simple fetch instead of Vercel AI SDK (documented as alternative)

---

## Phase 1: Design & Contracts (Complete)

**Outputs**:
- `data-model.md` - SQLModel definitions for Conversation and Message entities
- `contracts/chat-api.yaml` - OpenAPI specification for chat endpoints
- `contracts/tool-schemas.json` - MCP tool definitions (5 tools: add_task, list_tasks, update_task, delete_task, get_task)
- `quickstart.md` - Developer setup guide

**Data Model**:
- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, conversation_id, role, content, tool_call_id, tool_name, created_at
- Relationships: User 1:N Conversation 1:N Message
- Cascade delete: Deleting conversation removes all messages

**API Endpoints**:
- POST /api/chat/message - Send message and receive AI response
- GET /api/chat/conversations - List user's conversations
- GET /api/chat/conversations/{id} - Get conversation with messages
- DELETE /api/chat/conversations/{id} - Delete conversation

**Tool Definitions**:
- add_task(title, due_date?, priority?, notes?)
- list_tasks(status?, priority?, limit?)
- update_task(task_id, title?, status?, priority?, due_date?, notes?)
- delete_task(task_id)
- get_task(task_id)

---

## Constitution Check (Post-Design Re-evaluation)

*GATE: Final verification after Phase 1 design completion*

**Principle I - Spec-Driven Development**: ✅ PASS
- Specification complete with validated requirements
- Implementation plan documents all design decisions
- Tasks will trace back to spec user stories

**Principle II - Persistence Layer with Neon PostgreSQL**: ✅ PASS
- SQLModel definitions created for Conversation and Message
- Migration script documented in data-model.md
- All queries use SQLModel ORM (no raw SQL)

**Principle III - Monorepo Architecture**: ✅ PASS
- Backend structure: src/models/, src/services/, src/api/, src/tools/
- Frontend structure: app/chat/, components/chat/, lib/
- Clear separation maintained

**Principle IV - Code Quality Standards**: ✅ PASS
- Python: Type hints in SQLModel definitions, PEP 8 compliance planned
- TypeScript: Functional components, proper typing in contracts

**Principle V - Specification-First Workflow**: ✅ PASS
- Spec → Plan → (next: Tasks) workflow followed
- All design decisions documented before implementation

**Principle VI - RESTful API Standard**: ✅ PASS
- POST for message creation (non-idempotent)
- GET for retrieving conversations (idempotent)
- DELETE for conversation removal
- Proper HTTP status codes documented (200, 201, 400, 401, 403, 404, 429, 500)

**Principle VII - Multi-User Authentication & Authorization**: ✅ PASS
- JWT Bearer token required on all endpoints
- All queries filter by user_id
- Tool execution scoped to authenticated user
- Conversation ownership verified before operations

**Principle VIII - AI Chatbot Integration with Groq**: ✅ PASS
- Groq with Llama 3.3 (`llama-3.3-70b-versatile`)
- OpenAI SDK with base_url override pattern documented
- Chat Completions API (not Assistants API)
- Stateless design with database-backed history
- MCP tool definitions with proper schemas
- User data scoping enforced in tool execution

**Final Gate Result**: ✅ ALL PRINCIPLES SATISFIED - Ready for task generation

---

## Architectural Decisions

### Decision 1: Groq via OpenAI SDK Compatibility

**Context**: Need to integrate Groq's Llama 3.3 model for AI chatbot functionality.

**Decision**: Use OpenAI Python SDK with custom `base_url` pointing to Groq API.

**Rationale**:
- Groq provides OpenAI-compatible endpoints
- No need for custom HTTP client or SDK
- Standard patterns work without modification
- Tool calling fully supported

**Alternatives**:
- Custom HTTP client: Rejected due to unnecessary complexity
- Groq-specific SDK: Doesn't exist
- LangChain: Rejected due to abstraction overhead for our use case

**Consequences**:
- ✅ Faster development (reuse OpenAI patterns)
- ✅ Better maintainability (standard SDK)
- ⚠️ Dependency on Groq maintaining OpenAI compatibility
- ⚠️ Rate limits (30 req/min on free tier)

---

### Decision 2: Stateless Chat Architecture

**Context**: Need to design chat endpoint that scales horizontally.

**Decision**: Store all conversation history in PostgreSQL, retrieve on each request.

**Rationale**:
- Enables horizontal scaling (any backend instance can handle any request)
- Database is single source of truth
- No server-side session state to manage
- Aligns with serverless deployment model

**Alternatives**:
- In-memory sessions: Rejected due to scaling limitations
- Redis cache: Rejected as premature optimization (database sufficient for MVP)

**Consequences**:
- ✅ Horizontal scalability
- ✅ Simplified deployment
- ⚠️ Database query on every request (mitigated by indexing)
- ⚠️ Need to manage context window truncation

---

### Decision 3: Vercel AI SDK for Frontend

**Context**: Need React integration for chat interface.

**Decision**: Use Vercel AI SDK's `useChat` hook.

**Rationale**:
- Battle-tested chat UI patterns
- Handles message state, streaming, error handling
- Simple API, minimal boilerplate
- Alternative (simple fetch) documented for flexibility

**Alternatives**:
- @openai/chatkit-react: Explicitly excluded by requirements
- Custom implementation: More work, reinventing the wheel

**Consequences**:
- ✅ Faster frontend development
- ✅ Built-in streaming support
- ⚠️ Additional dependency (acceptable tradeoff)

---

## 📋 Architectural Decision Records

**Significant decisions detected** that warrant ADR documentation:

1. **Groq Integration Pattern**: Using OpenAI SDK compatibility vs custom client
   - Impact: Long-term dependency on Groq's API compatibility
   - Alternatives: Multiple options considered
   - Scope: Cross-cutting (affects all AI interactions)

2. **Stateless Chat Architecture**: Database-backed history vs session state
   - Impact: Affects scalability and deployment model
   - Alternatives: In-memory sessions, Redis cache
   - Scope: Cross-cutting (affects backend architecture)

**Recommendation**: Document these decisions with:
```
/sp.adr groq-integration-openai-sdk-pattern
/sp.adr stateless-chat-database-backed-history
```

Or combine into single ADR:
```
/sp.adr ai-chatbot-architecture-decisions
```

---

## Next Steps

1. ✅ Phase 0 (Research) - Complete
2. ✅ Phase 1 (Design & Contracts) - Complete
3. ⏭️ Run `/sp.tasks` to generate implementation tasks
4. ⏭️ Implement tasks in priority order (P1 → P2 → P3)
5. ⏭️ Consider documenting ADRs for architectural decisions

---

## Summary

**Planning Complete**: All design artifacts generated and validated against constitution.

**Artifacts Created**:
- research.md (technical decisions)
- data-model.md (database schema)
- contracts/chat-api.yaml (REST API spec)
- contracts/tool-schemas.json (MCP tools)
- quickstart.md (developer guide)

**Ready for Implementation**: All principles satisfied, no blockers identified.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical research)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoints
│   └── tool-schemas.json # Tool calling schemas for MCP
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # Conversation SQLModel
│   │   ├── message.py           # Message SQLModel
│   │   └── task.py              # Existing Task model (Phase 2)
│   ├── services/
│   │   ├── chat_service.py      # Chat orchestration logic
│   │   ├── groq_client.py       # Groq API client wrapper
│   │   └── tool_executor.py     # Tool calling execution engine
│   ├── api/
│   │   ├── chat.py              # Chat endpoints (POST /chat/message, etc.)
│   │   └── conversations.py     # Conversation management endpoints
│   ├── tools/
│   │   ├── task_tools.py        # MCP tool definitions (add_task, list_tasks, etc.)
│   │   └── tool_registry.py     # Tool registration and schema management
│   └── auth/
│       └── jwt_middleware.py    # Existing JWT verification (Phase 2)
└── tests/
    ├── unit/
    │   ├── test_chat_service.py
    │   ├── test_tool_executor.py
    │   └── test_groq_client.py
    ├── integration/
    │   ├── test_chat_api.py
    │   └── test_tool_execution.py
    └── contract/
        └── test_chat_contracts.py

frontend/
├── src/
│   ├── app/
│   │   ├── chat/
│   │   │   ├── page.tsx         # Chat interface page
│   │   │   └── layout.tsx       # Chat layout wrapper
│   │   └── api/
│   │       └── chat/
│   │           └── route.ts     # Next.js API route proxy (optional)
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx    # Main chat component
│   │   │   ├── MessageList.tsx      # Message display
│   │   │   ├── MessageInput.tsx     # User input field
│   │   │   └── ToolCallDisplay.tsx  # Tool execution visualization
│   │   └── ui/
│   │       └── [existing UI components]
│   └── lib/
│       ├── chat-client.ts       # API client for chat endpoints
│       └── types.ts             # TypeScript types for chat
└── tests/
    └── components/
        └── chat/
            └── ChatInterface.test.tsx
```

**Structure Decision**: Monorepo architecture as mandated by Constitution Principle III. Backend uses FastAPI with modular service layer separating chat orchestration, Groq client, and tool execution. Frontend uses Next.js App Router with dedicated chat page and reusable components. Tool definitions follow MCP pattern in dedicated `tools/` module.

## Complexity Tracking

> **No violations detected** - All constitution principles satisfied without exceptions.
