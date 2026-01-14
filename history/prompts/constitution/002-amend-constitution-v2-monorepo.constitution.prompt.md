---
id: 002
title: Amend constitution to v2.0.0 monorepo architecture
stage: constitution
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-phase1-todo-cli
user: HP
command: /sp.constitution
labels: ["constitution", "amendment", "architecture", "monorepo", "persistence", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/tasks-template.md
  - CLAUDE.md
tests:
  - N/A (documentation update)
---

## Prompt

```text
AMENDMENT:
1. **Architecture Update:** Transition to a Monorepo structure.
   - `/frontend`: Next.js 16+ (App Router), Tailwind CSS.
   - `/backend`: Python FastAPI.
2. **Persistence:** REVOKE "In-Memory" constraint. MANDATE Neon Serverless PostgreSQL using SQLModel ORM.
3. **Authentication:** Implement "Better Auth" with JWT tokens. The Backend must verify tokens via a shared secret.
4. **API Standard:** All data access must go through RESTful API endpoints (GET, POST, PUT, DELETE, PATCH).
5. **Multi-User:** Data must be scoped to the authenticated `user_id`.
```

## Response snapshot

**Version Change**: 1.0.0 → 2.0.0 (MAJOR bump)

**Rationale**: The amendments fundamentally REVOKE Principle II (In-Memory Storage constraint), representing a backward-incompatible governance change. Complete architectural shift from single-project CLI to monorepo full-stack application.

**Modified Principles**:
- Principle II: "In-Memory Storage (Phase 1 Constraint)" → "Persistence Layer with Neon PostgreSQL" (in-memory constraint REVOKED)
- Principle III: "Python 3.13+ with UV" → "Monorepo Architecture with Multi-Technology Stack"

**Added Principles**:
- Principle VI: RESTful API Standard (mandates HTTP methods, status codes, contract documentation)
- Principle VII: Multi-User Authentication & Authorization (Better Auth, JWT, user-scoped data)

**Updated Artifacts**:
1. `.specify/memory/constitution.md` - Complete rewrite with new principles and expanded governance
2. `.specify/templates/plan-template.md` - Enhanced monorepo structure with FastAPI/Next.js details
3. `.specify/templates/tasks-template.md` - Added monorepo path conventions
4. `CLAUDE.md` - Updated Active Technologies section to reflect v2.0.0 stack

**Sync Impact Report** (embedded in constitution.md):
- Templates ✅ Updated for monorepo patterns
- Follow-up TODOs: Migration plan needed for Phase 1 code, frontend scaffolding, Better Auth integration

## Outcome

- ✅ Impact: MAJOR architectural governance change from in-memory CLI to full-stack monorepo with persistence, authentication, and RESTful API
- 🧪 Tests: N/A (documentation amendment)
- 📁 Files: 4 files modified (constitution, 2 templates, CLAUDE.md)
- 🔁 Next prompts: Suggest ADR for architecture decision; Plan migration from Phase 1 CLI to FastAPI backend; Design Better Auth integration; Specify Neon PostgreSQL schema
- 🧠 Reflection: Constitutional amendment executed successfully with comprehensive template propagation. Version bump rationale clear (REVOKED principle = MAJOR). Sync Impact Report provides actionable follow-up TODOs.

## Evaluation notes (flywheel)

- Failure modes observed: None - shell script unavailable but agent-native PHR creation succeeded
- Graders run and results (PASS/FAIL): Manual validation PASS (all placeholders filled, routing correct, no unresolved tokens)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate that `/sp.plan` and `/sp.tasks` commands properly leverage new constitution principles when generating artifacts
