# ADR-001: Monorepo Architecture with Workspace Separation

**Status**: Accepted
**Date**: 2026-01-05
**Deciders**: Architecture Team
**Feature**: 002-phase2-fullstack-todo

## Context

Phase 2 transforms the Todo App from a single-user CLI to a full-stack multi-user web application. We need an architecture that:

1. Supports polyglot development (Python backend, TypeScript frontend)
2. Enables independent deployment of frontend and backend
3. Facilitates atomic commits when API contracts change
4. Maintains clear separation of concerns
5. Complies with Constitution v2.0.0 Principle III (Monorepo mandate)
6. Provides consistent development environment across team

**Constraints**:
- Constitution mandates `/frontend` and `/backend` workspaces at repository root
- Backend: Python FastAPI with UV dependency management
- Frontend: Next.js 16+ with npm dependency management
- Need Docker Compose orchestration for local development

## Decision

Adopt a **workspace-based monorepo** structure with the following components:

### Repository Structure
```
/
├── frontend/              # Next.js 16+ workspace
│   ├── package.json      # npm dependencies
│   ├── src/app/          # App Router
│   └── Dockerfile
├── backend/               # FastAPI workspace
│   ├── pyproject.toml    # UV dependencies
│   ├── src/              # Python modules
│   └── Dockerfile
├── specs/                 # Shared specifications
├── docker-compose.yml     # Orchestration
└── README.md
```

### Key Components:

1. **Independent Workspaces**: Frontend and backend maintain separate dependency management
2. **Shared Documentation**: Specifications and API contracts in `/specs`
3. **Docker Compose**: PostgreSQL + Backend + Frontend services with hot reload
4. **No Monorepo Tooling**: Avoid Turborepo/Nx complexity for two-workspace project

### Deployment Model:
- **Frontend**: Deployed independently (Vercel, Netlify, etc.)
- **Backend**: Deployed independently (Docker containers on cloud platforms)
- **Database**: Neon Serverless PostgreSQL (managed)

## Consequences

### Positive

✅ **Constitution Compliance**: Satisfies Principle III mandate for `/frontend` and `/backend` separation

✅ **Atomic Commits**: Changes to API contracts can be committed atomically across frontend and backend, reducing integration drift

✅ **Independent Deployment**: Frontend and backend can scale and deploy independently, enabling faster iteration cycles

✅ **Clear Ownership**: Workspace boundaries make code ownership and review straightforward

✅ **Simplified Tooling**: No complex monorepo tools needed for two workspaces, reducing onboarding and maintenance burden

✅ **Hot Reload**: Docker Compose volumes enable instant feedback during development

### Negative

⚠️ **Manual Synchronization**: No automated dependency graph between workspaces - developers must manually ensure API contract compatibility

⚠️ **Deployment Coordination**: Breaking API changes require coordinated frontend + backend deployments (mitigated by API versioning)

⚠️ **Docker Dependency**: Local development requires Docker Desktop, which has licensing costs for enterprise teams

⚠️ **Build Time**: Building both workspaces from scratch takes longer than a single-language project (mitigated by Docker layer caching)

### Risks

🔴 **Risk**: API contract drift if frontend and backend diverge
- **Mitigation**: OpenAPI spec in `/specs/<feature>/contracts/` as single source of truth, contract tests enforce compliance

🟡 **Risk**: Docker Compose complexity for new developers
- **Mitigation**: Comprehensive `quickstart.md` with troubleshooting, one-command setup (`docker compose up`)

## Alternatives Considered

### Alternative 1: Turborepo/Nx Monorepo Tools

**Pros**:
- Automated build orchestration and caching
- Task dependency graphs prevent out-of-order builds
- Integrated CI/CD pipelines

**Cons**:
- Over-engineered for two workspaces
- Adds significant configuration complexity
- Requires team learning curve for tooling
- Adds build-time dependencies

**Why Rejected**: Complexity outweighs benefits for a two-workspace monorepo. Simple workspace separation suffices.

### Alternative 2: Separate Repositories (Polyrepo)

**Pros**:
- Complete independence between frontend and backend
- Simpler CI/CD (each repo has own pipeline)
- No shared tooling requirements

**Cons**:
- **Violates Constitution Principle III** (monorepo mandate)
- API contract sync becomes manual and error-prone
- Atomic commits across API changes impossible
- Duplicated documentation (specs, ADRs)

**Why Rejected**: Constitution violation is a hard blocker. Loss of atomic commits significantly increases integration risk.

### Alternative 3: Git Submodules

**Pros**:
- Separate repository independence
- Can appear as monorepo structure

**Cons**:
- Adds Git complexity (submodule update commands)
- Harder to maintain atomic commits
- Confusing for developers unfamiliar with submodules
- Poor DX (developer experience)

**Why Rejected**: Complexity and poor DX outweigh benefits. Submodules are notoriously difficult to manage correctly.

## References

- [Constitution v2.0.0 Principle III](../../.specify/memory/constitution.md#principle-iii-monorepo-architecture-with-multi-technology-stack)
- [Implementation Plan: Monorepo Structure](../../specs/002-phase2-fullstack-todo/plan.md#project-structure)
- [Research: Monorepo Structure for Next.js + FastAPI](../../specs/002-phase2-fullstack-todo/research.md#1-monorepo-structure-for-nextjs--fastapi)
- [Quickstart Guide: Docker Compose Setup](../../specs/002-phase2-fullstack-todo/quickstart.md)

## Notes

- This decision is **reversible** but would require significant refactoring (moving all code)
- Future features will follow this same monorepo pattern per Constitution
- If the project grows beyond 5 workspaces, revisit Turborepo/Nx decision
