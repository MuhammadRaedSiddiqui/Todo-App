---
id: 003
title: Refactor Phase 2 monorepo structure
stage: general
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-phase1-todo-cli
user: HP
command: manual
labels: ["refactoring", "monorepo", "structure", "phase2", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/pyproject.toml
  - backend/.env.example
  - backend/README.md
  - backend/src/__init__.py
  - backend/src/main.py
  - backend/src/models/__init__.py
  - backend/src/services/__init__.py
  - backend/src/api/__init__.py
  - backend/src/auth/__init__.py
  - frontend/package.json
  - frontend/.env.example
  - frontend/README.md
  - frontend/tsconfig.json
  - frontend/next.config.js
  - frontend/tailwind.config.js
  - frontend/src/app/layout.tsx
  - frontend/src/app/page.tsx
  - frontend/src/app/globals.css
  - .gitignore
  - README.md
  - legacy_phase1/README.md
tests:
  - N/A (structure refactor)
---

## Prompt

```text
Refactor the project structure for Phase 2. Create two main folders: frontend and backend. Move the existing Phase 1 Python code into a legacy_phase1 folder so we keep it for reference but start fresh for Phase 2.
```

## Response snapshot

Successfully refactored project structure from Phase 1 single-project to Phase 2 monorepo architecture per Constitution v2.0.0.

**Actions Completed**:

1. **Created Monorepo Structure**:
   - `frontend/` - Next.js 16+ application
   - `backend/` - FastAPI application
   - `legacy_phase1/` - Phase 1 code preserved for reference

2. **Backend Initialization** (`backend/`):
   - FastAPI project structure with `src/models`, `src/services`, `src/api`, `src/auth`
   - Test directories: `tests/unit`, `tests/integration`, `tests/contract`
   - `pyproject.toml` with FastAPI, SQLModel, psycopg2, python-jose dependencies
   - `.env.example` template for DATABASE_URL and JWT configuration
   - Basic FastAPI app in `src/main.py` with CORS and health check endpoints
   - Comprehensive README.md with setup instructions

3. **Frontend Initialization** (`frontend/`):
   - Next.js 16+ project structure with App Router (`src/app/`)
   - `src/components/` and `src/lib/` directories
   - `package.json` with Next.js 16, React 19, Better Auth, Tailwind CSS
   - TypeScript configuration (`tsconfig.json`)
   - Tailwind CSS configuration
   - Basic App Router pages (`layout.tsx`, `page.tsx`, `globals.css`)
   - `.env.example` template for API URL and Better Auth
   - Comprehensive README.md with setup instructions

4. **Legacy Phase 1 Preservation**:
   - Moved `src/`, `tests/`, `pyproject.toml`, `phase1_requirements.md` to `legacy_phase1/`
   - Created `legacy_phase1/README.md` explaining Phase 1 code is reference-only

5. **Configuration Updates**:
   - Updated `.gitignore` with frontend (node_modules, .next, .env.local) and backend (.env, __pycache__, alembic) entries
   - Created comprehensive root `README.md` with monorepo architecture documentation

**Directory Structure** (final):
```
todo-app/
├── backend/              # FastAPI backend
│   ├── src/             # models, services, api, auth
│   ├── tests/           # unit, integration, contract
│   └── pyproject.toml
├── frontend/            # Next.js 16+ frontend
│   ├── src/app/         # App Router
│   └── package.json
├── legacy_phase1/       # Phase 1 CLI (reference)
│   ├── src/
│   └── tests/
├── specs/               # Feature specs (SDD)
├── history/             # PHRs, ADRs
└── .specify/            # Templates
```

**Constitution Compliance**: Phase 2 structure fully complies with Constitution v2.0.0 Principle III (Monorepo Architecture).

## Outcome

- ✅ Impact: Complete project restructure from Phase 1 single-project to Phase 2 monorepo with frontend/backend separation
- 🧪 Tests: N/A (structure refactor, no tests modified)
- 📁 Files: 20 files created (backend scaffold, frontend scaffold, READMEs, configs), 4 files moved to legacy_phase1/
- 🔁 Next prompts: Set up Neon PostgreSQL database; Implement Better Auth; Create SQLModel schemas; Build API endpoints; Develop frontend authentication flow
- 🧠 Reflection: Clean separation achieved between Phase 1 (legacy) and Phase 2 (active). Both workspaces have comprehensive READMEs. Monorepo structure enables parallel frontend/backend development per Constitution v2.0.0.

## Evaluation notes (flywheel)

- Failure modes observed: None - structure refactor completed successfully
- Graders run and results (PASS/FAIL): Manual validation PASS (directories created, files in correct locations, .gitignore updated, READMEs comprehensive)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Initialize UV for backend (`cd backend && uv sync`) and npm for frontend (`cd frontend && npm install`) to validate dependency management
