---
id: 002
title: AI Chatbot Implementation Planning
stage: plan
date: 2026-01-18
surface: agent
model: claude-sonnet-4-5
feature: 003-ai-chatbot
branch: 003-ai-chatbot
user: user
command: /sp.plan
labels: ["plan", "ai-chatbot", "groq", "architecture", "phase-3", "mcp-tools"]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot/plan.md
  - specs/003-ai-chatbot/research.md
  - specs/003-ai-chatbot/data-model.md
  - specs/003-ai-chatbot/contracts/chat-api.yaml
  - specs/003-ai-chatbot/contracts/tool-schemas.json
  - specs/003-ai-chatbot/quickstart.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

Architect the Phase 3 AI Integration (Groq Edition).

## Critical Implementation Details
1. **The "Fake OpenAI" Pattern:** - Explain how to initialize `client = OpenAI(base_url="...", api_key="...")` using Groq credentials.
   - Define the model constant: `MODEL = "llama-3.3-70b-versatile"`.
2. **MCP Tooling:** - Define the schema for `add_task`, `list_tasks`, etc., in the standard format Groq expects.
3. **Frontend Strategy:** - Plan a simple Chat Interface in Next.js (using `useChat` from Vercel AI SDK or simple `fetch`).
   - Do NOT use `@openai/chatkit-react`.

## Database Schema
- `Conversation`: id, user_id, created_at.
- `Message`: id, conversation_id, role (user/assistant/tool), content.

## Response snapshot

Completed comprehensive implementation plan for AI Chatbot (Phase 3) with full architecture design.

**Phase 0 - Research (research.md)**:
- Groq integration pattern: OpenAI SDK with base_url override
- Tool calling schemas: 5 MCP tools (add_task, list_tasks, update_task, delete_task, get_task)
- Frontend strategy: Vercel AI SDK useChat hook
- Database design: Two-table schema (Conversation, Message)
- Stateless architecture: Database-backed conversation history

**Phase 1 - Design & Contracts**:
- **data-model.md**: SQLModel definitions with relationships, migrations, validation rules
- **contracts/chat-api.yaml**: OpenAPI spec for 4 endpoints (POST /chat/message, GET /conversations, GET /conversations/{id}, DELETE /conversations/{id})
- **contracts/tool-schemas.json**: Complete MCP tool schemas with parameter validation
- **quickstart.md**: Developer setup guide with troubleshooting, deployment, and optimization sections

**Technical Context**:
- Backend: Python 3.13+, FastAPI, SQLModel, OpenAI SDK (Groq), Pydantic
- Frontend: Next.js 16+, React, Vercel AI SDK, Tailwind CSS
- Database: Neon PostgreSQL (Conversation, Message tables)
- Performance: <5s response time (95%), <3s for simple queries
- Constraints: Groq free tier (30 req/min), ~8K token context window

**Project Structure**:
- Backend: src/models/, src/services/, src/api/, src/tools/
- Frontend: app/chat/, components/chat/, lib/
- Monorepo architecture maintained

**Constitution Check**: All 8 principles validated (Spec-Driven Development, PostgreSQL persistence, Monorepo architecture, Code quality, Specification-first workflow, RESTful API, Multi-user auth, AI chatbot integration with Groq)

**Architectural Decisions**:
1. Groq via OpenAI SDK compatibility (vs custom client)
2. Stateless chat architecture (database-backed vs session state)
3. Vercel AI SDK for frontend (vs custom implementation)

**ADR Recommendations**: Suggested documenting 2 significant architectural decisions (Groq integration pattern, stateless architecture)

## Outcome

- ✅ Impact: Complete implementation plan with all design artifacts ready for task generation
- 🧪 Tests: No tests at planning stage (tests will be defined in tasks.md)
- 📁 Files: plan.md, research.md, data-model.md, chat-api.yaml, tool-schemas.json, quickstart.md, CLAUDE.md updated
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks, optionally `/sp.adr` to document architectural decisions
- 🧠 Reflection: Successfully architected stateless AI chatbot with Groq integration following MCP pattern. All constitution principles satisfied. Clear separation between research (Phase 0) and design (Phase 1) artifacts.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning process completed successfully
- Graders run and results (PASS/FAIL): Constitution Check PASS (8/8 principles), Post-design re-evaluation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
