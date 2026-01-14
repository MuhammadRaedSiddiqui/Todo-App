# Todo App v2.0

Multi-user todo application with Next.js frontend and FastAPI backend.

## Architecture (Constitution v2.0.0)

This project follows a **monorepo structure** with clear separation between frontend and backend:

- **Frontend**: Next.js 16+ (App Router), React, TypeScript, Tailwind CSS, Better Auth
- **Backend**: Python FastAPI, SQLModel ORM, Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens (shared secret verification)
- **API**: RESTful endpoints (GET, POST, PUT, PATCH, DELETE)
- **Multi-User**: All data scoped to authenticated `user_id`

## Project Structure

```
todo-app/
├── frontend/              # Next.js 16+ frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities, API clients
│   ├── tests/
│   ├── package.json
│   └── README.md
│
├── backend/               # FastAPI backend
│   ├── src/
│   │   ├── models/       # SQLModel classes (Neon PostgreSQL)
│   │   ├── services/     # Business logic
│   │   ├── api/          # RESTful endpoints
│   │   └── auth/         # JWT verification
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── contract/
│   ├── pyproject.toml
│   └── README.md
│
├── legacy_phase1/         # Phase 1 CLI code (reference only)
│   ├── src/
│   ├── tests/
│   └── pyproject.toml
│
├── specs/                 # Feature specifications (SDD)
├── history/               # Prompt History Records, ADRs
├── .specify/              # SpecKit Plus templates
└── CLAUDE.md              # Claude Code project rules
```

## Quick Start

### Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Configure DATABASE_URL and JWT_SECRET_KEY in .env
uvicorn src.main:app --reload
```

Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Configure NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET in .env.local
npm run dev
```

Frontend runs at: http://localhost:3000

## Development Workflow (Constitution v2.0.0)

This project follows **Spec-Driven Development (SDD)**:

1. **Specification First**: Create `specs/<feature>/spec.md` before writing code
2. **Planning**: Generate `specs/<feature>/plan.md` with architecture decisions
3. **Tasks**: Create `specs/<feature>/tasks.md` with testable implementation steps
4. **Implementation**: Follow priority order (P1 → P2 → P3)
5. **Testing**: Unit, integration, and contract tests required
6. **Review**: Verify spec compliance and constitution adherence

### Constitution Principles

- **Principle I**: Spec-Driven Development (all code traceable to specs)
- **Principle II**: Neon PostgreSQL with SQLModel ORM
- **Principle III**: Monorepo architecture (Next.js + FastAPI)
- **Principle IV**: Code quality standards (PEP 8, ESLint, type safety)
- **Principle V**: Specification-first workflow
- **Principle VI**: RESTful API standard
- **Principle VII**: Multi-user authentication with JWT

See `.specify/memory/constitution.md` for full details.

## Phase 1 → Phase 2 Migration

Phase 1 code (in-memory CLI) has been preserved in `legacy_phase1/` for reference.

Phase 2 introduces:
- ✅ Monorepo structure
- ✅ Next.js 16+ frontend with Tailwind CSS
- ✅ FastAPI backend
- ✅ Neon PostgreSQL persistence (REVOKED in-memory constraint)
- ✅ Better Auth with JWT
- ✅ Multi-user support with user-scoped data
- ✅ RESTful API

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

- **Constitution**: `.specify/memory/constitution.md`
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`
- **Feature Specs**: `specs/<feature>/spec.md`
- **API Contracts**: `specs/<feature>/contracts/`
- **ADRs**: `history/adr/`

## Technology Stack

**Frontend**:
- Next.js 16+ (App Router)
- React 19 with TypeScript
- Tailwind CSS
- Better Auth

**Backend**:
- Python 3.13+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- JWT authentication

**Development Tools**:
- UV (Python dependency management)
- ESLint + Prettier
- Ruff (Python linting)
- pytest (Python testing)

## Contributing

1. Follow Spec-Driven Development workflow
2. Create feature spec before implementation
3. Ensure all tests pass
4. Verify constitution compliance
5. Reference Task IDs in commits

## License

[Add license information]
