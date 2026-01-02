<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial creation)
- Added principles: 5 (all from user input)
- Removed sections: N/A (constitution newly created)
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ No changes needed (Constitution Check section already references constitution file)
  - .specify/templates/spec-template.md ✅ No changes needed (aligns with spec-first workflow)
  - .specify/templates/tasks-template.md ✅ No changes needed (task IDs reference specs)
- Follow-up TODOs: None
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

### II. In-Memory Storage (Phase 1 Constraint)
For Phase 1, the application MUST store all data in-memory using Python lists or dictionaries.
No database or file persistence is permitted until Phase 2. Data structures MUST be designed
with clean separation to facilitate future persistence layer replacement.

**Rationale**: Phase 1 focuses on core functionality and CLI experience. The in-memory constraint
simplifies development and allows rapid iteration. Clean separation ensures Phase 2 migration
is straightforward.

### III. Python 3.13+ with UV
The project MUST use Python 3.13 or higher. All dependencies MUST be managed via UV package
manager. Dependencies MUST be declared in `pyproject.toml` with locked versions in
`uv.lock`.

**Rationale**: UV provides fast, reliable dependency management. Python 3.13 ensures access to
latest language features and performance improvements.

### IV. Code Quality Standards
All code MUST follow PEP 8 style guidelines. The codebase MUST use modular design with clear
separation of concerns. Functions and classes MUST have single responsibilities. CLI interface
logic MUST be separate from business logic and models.

**Rationale**: Clean, modular code reduces technical debt, improves testability, and makes the
project accessible to new contributors. PEP 8 compliance ensures consistency.

### V. Specification-First Workflow
Every feature MUST be defined in `specs/<feature>/spec.md` before implementation begins. The spec
MUST include user stories with priorities (P1, P2, P3), acceptance criteria, and edge cases.
Tasks in `specs/<feature>/tasks.md` MUST reference the originating spec and user story.

**Rationale**: Writing specifications before coding catches edge cases early, clarifies requirements
with stakeholders, and creates an implementation roadmap. This prevents scope creep and
ensures deliverable quality.

## Development Workflow

### Pre-Implementation Requirements
Before writing any production code:
1. Create feature specification in `specs/<feature-name>/spec.md`
2. Generate implementation plan in `specs/<feature-name>/plan.md`
3. Create task list in `specs/<feature-name>/tasks.md`
4. Obtain sign-off on specification (if applicable)

### Implementation Standards
- Tasks MUST be implemented in priority order (P1 → P2 → P3)
- Each task MUST include corresponding tests
- Commit messages MUST reference Task ID (e.g., `[T001] Add task model`)
- Code reviews MUST verify spec compliance

### Testing Requirements
- Unit tests for all model and service functions
- Integration tests for CLI workflows
- Error cases MUST be tested explicitly

## Quality Gates

All pull requests and code reviews MUST verify:
- [ ] Code traces to Task ID in `tasks.md`
- [ ] Implementation matches specification in `spec.md`
- [ ] PEP 8 compliance (use linter)
- [ ] Tests pass for all modified code
- [ ] Error handling covers edge cases from spec
- [ ] No hardcoded values that should be configuration

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of proposed changes
2. Review and approval
3. Update to constitution version following semantic versioning

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
