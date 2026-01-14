<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0 (MAJOR - backward-incompatible governance change)
- Modified principles:
  - Principle II: "In-Memory Storage (Phase 1 Constraint)" → "Persistence Layer with Neon PostgreSQL" (REVOKED in-memory constraint)
  - Principle III: "Python 3.13+ with UV" → "Monorepo Architecture with Multi-Technology Stack"
- Added principles:
  - Principle VI: RESTful API Standard
  - Principle VII: Multi-User Authentication & Authorization
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ Updated (monorepo structure options expanded)
  - .specify/templates/spec-template.md ✅ No changes needed (technology-agnostic user stories)
  - .specify/templates/tasks-template.md ✅ Updated (monorepo path conventions added)
- Follow-up TODOs:
  - Migration plan needed for existing Phase 1 in-memory code to FastAPI + PostgreSQL
  - Frontend implementation using Next.js 16+ App Router needs initial scaffolding
  - Better Auth integration and JWT verification setup required
-->

# Todo App Constitution

## Core Principles

### I. Spec-Driven Development
All code changes MUST be traceable to a Task ID and Spec reference. No production code is written
without first creating a feature specification in `specs/<feature>/spec.md` and corresponding tasks
in `specs/<feature>/tasks.md`. This ensures every implementation decision is documented and
reviewable.

**Rationale**: Spec-Driven Development creates a single source of truth for feature behavior,
enables parallel work streams, and provides documentation for future maintainers.

### II. Persistence Layer with Neon PostgreSQL
The application MUST use Neon Serverless PostgreSQL as the persistence layer. All data access
MUST be implemented using SQLModel ORM for type-safe database operations. The in-memory storage
constraint from Phase 1 is hereby REVOKED. Data models MUST be defined as SQLModel classes with
proper relationships, constraints, and migrations.

**Rationale**: Neon Serverless PostgreSQL provides scalable, managed persistence without
infrastructure overhead. SQLModel combines Pydantic validation with SQLAlchemy ORM, ensuring
type safety and reducing boilerplate. This architectural shift enables multi-user support and
production-ready data durability.

### III. Monorepo Architecture with Multi-Technology Stack
The project MUST follow a monorepo structure with clear separation between frontend and backend:
- **Frontend** (`/frontend`): Next.js 16+ using App Router, styled with Tailwind CSS
- **Backend** (`/backend`): Python 3.13+ with FastAPI framework, SQLModel ORM, and Neon PostgreSQL

Each workspace MUST maintain its own dependency management (Node.js packages for frontend,
Python packages via UV for backend). Shared types and contracts MUST be documented in
`specs/<feature>/contracts/`.

**Rationale**: Monorepo architecture enables atomic commits across frontend and backend,
simplifies dependency management, and provides a single source of truth for API contracts.
The technology choices leverage modern frameworks optimized for developer experience and
performance.

### IV. Code Quality Standards
All code MUST follow language-specific best practices:
- **Python**: PEP 8 style, type hints, modular design with single responsibility
- **TypeScript/React**: ESLint + Prettier, functional components, proper type safety

The codebase MUST use modular design with clear separation of concerns. Functions and classes
MUST have single responsibilities. API endpoint logic MUST be separate from business logic
and data models. Frontend components MUST separate presentation from business logic.

**Rationale**: Clean, modular code reduces technical debt, improves testability, and makes the
project accessible to new contributors. Language-specific standards ensure consistency within
each technology domain.

### V. Specification-First Workflow
Every feature MUST be defined in `specs/<feature>/spec.md` before implementation begins. The spec
MUST include user stories with priorities (P1, P2, P3), acceptance criteria, and edge cases.
Tasks in `specs/<feature>/tasks.md` MUST reference the originating spec and user story.

**Rationale**: Writing specifications before coding catches edge cases early, clarifies requirements
with stakeholders, and creates an implementation roadmap. This prevents scope creep and
ensures deliverable quality.

### VI. RESTful API Standard
All data operations MUST be exposed through RESTful API endpoints in the FastAPI backend.
The API MUST implement standard HTTP methods:
- **GET**: Retrieve resources (read-only, idempotent)
- **POST**: Create new resources
- **PUT**: Replace existing resources (full update)
- **PATCH**: Partially update resources
- **DELETE**: Remove resources

All endpoints MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500).
API contracts MUST be documented in `specs/<feature>/contracts/` with request/response schemas.

**Rationale**: RESTful API design provides a predictable, standardized interface between frontend
and backend. Standard HTTP semantics ensure the API is intuitive and follows web conventions.
Explicit contracts enable parallel frontend/backend development and prevent integration issues.

### VII. Multi-User Authentication & Authorization
The application MUST implement user authentication using Better Auth with JWT (JSON Web Token)
strategy. The backend MUST verify JWT tokens using a shared secret configured via environment
variables. All API endpoints MUST enforce authentication where required. All data MUST be scoped
to the authenticated `user_id` to ensure multi-tenant isolation.

**Rationale**: Better Auth provides modern authentication patterns with minimal configuration.
JWT tokens enable stateless authentication suitable for serverless deployments. User-scoped
data ensures privacy and security in multi-user environments. Shared secret verification
maintains security without coupling frontend and backend authentication implementations.

## Development Workflow

### Pre-Implementation Requirements
Before writing any production code:
1. Create feature specification in `specs/<feature-name>/spec.md`
2. Generate implementation plan in `specs/<feature-name>/plan.md`
3. Create task list in `specs/<feature-name>/tasks.md`
4. Document API contracts in `specs/<feature-name>/contracts/` (if applicable)
5. Obtain sign-off on specification (if applicable)

### Implementation Standards
- Tasks MUST be implemented in priority order (P1 → P2 → P3)
- Each task MUST include corresponding tests (unit, integration, or contract tests)
- Commit messages MUST reference Task ID (e.g., `[T001] Add task model`)
- Code reviews MUST verify spec compliance
- API changes MUST update contract documentation before implementation
- Database migrations MUST be versioned and reversible

### Testing Requirements
- **Backend**: Unit tests for models and services, integration tests for API endpoints, contract tests for API schemas
- **Frontend**: Component tests for UI, integration tests for user workflows, E2E tests for critical paths
- Error cases MUST be tested explicitly
- Authentication and authorization flows MUST have dedicated test coverage

## Quality Gates

All pull requests and code reviews MUST verify:
- [ ] Code traces to Task ID in `tasks.md`
- [ ] Implementation matches specification in `spec.md`
- [ ] Language-specific linting passes (PEP 8 for Python, ESLint for TypeScript)
- [ ] Tests pass for all modified code
- [ ] Error handling covers edge cases from spec
- [ ] No hardcoded secrets or tokens (use environment variables)
- [ ] API contracts match documented schemas
- [ ] Database migrations are reversible
- [ ] User data is properly scoped to `user_id`
- [ ] Authentication flows are secure (JWT verification, HTTPS in production)

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of proposed changes with clear rationale
2. Review and approval by project stakeholders
3. Update to constitution version following semantic versioning:
   - **MAJOR**: Backward-incompatible principle removals or redefinitions
   - **MINOR**: New principles/sections added or materially expanded guidance
   - **PATCH**: Clarifications, wording improvements, non-semantic refinements

**Version**: 2.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-05
