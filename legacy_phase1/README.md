# Phase 1 - Legacy Code (Reference Only)

This directory contains the original Phase 1 implementation of the Todo CLI application.

## ⚠️ IMPORTANT: This code is for reference only

Phase 1 has been **superseded by Constitution v2.0.0** which mandates:
- Monorepo structure (`/frontend` and `/backend`)
- Next.js 16+ frontend
- FastAPI backend
- Neon PostgreSQL (REVOKED in-memory constraint)
- Better Auth with JWT
- Multi-user support

## Phase 1 Implementation

Phase 1 was a **Python CLI application** with:
- In-memory storage (list of dictionaries)
- Simple CLI menu interface
- Basic CRUD operations (Create, Read, Update, Delete)
- No persistence (data lost on exit)
- Single-user only

## Original Structure

```
src/
├── cli/
│   └── menu.py         # CLI interface
├── models/
│   └── task.py         # Task model (dict-based)
├── services/
│   └── task_service.py # Business logic
└── main.py             # Entry point

tests/
├── unit/               # Unit tests
└── integration/        # Integration tests
```

## Running Phase 1 (For Reference)

If you need to run the Phase 1 code:

```bash
cd legacy_phase1
uv sync
python -c "from src.services.task_service import TaskService; from src.cli.menu import TodoMenu; service = TaskService(); menu = TodoMenu(service); import sys; sys.stdin = open('/dev/tty' if os.name != 'nt' else 'CON')"
```

## Migration to Phase 2

Phase 1 code has been archived here. All new development should follow:
- **Backend**: `../backend/` (FastAPI + Neon PostgreSQL)
- **Frontend**: `../frontend/` (Next.js 16+ with Better Auth)
- **Constitution**: `../.specify/memory/constitution.md` (v2.0.0)

See the root `README.md` for Phase 2 architecture and setup instructions.
