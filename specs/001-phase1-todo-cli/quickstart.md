# Quickstart Guide: Phase 1 In-Memory Todo CLI

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

1. **Initialize UV project** (if not already done):
   ```bash
   uv init --python 3.13
   ```

2. **Sync dependencies**:
   ```bash
   uv sync
   ```

3. **Verify Python version**:
   ```bash
   python --version
   # Expected: Python 3.13.x
   ```

## Running the Application

### Development Mode

```bash
python src/main.py
```

### From Source

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows

# Run application
python src/main.py
```

## Project Structure

```
todo-app/
├── src/
│   ├── main.py            # Entry point
│   ├── cli/
│   │   └── menu.py        # CLI interface
│   ├── models/
│   │   └── task.py        # Task data structure
│   └── services/
│       └── task_service.py # Business logic
├── tests/
│   ├── unit/
│   │   ├── test_task.py
│   │   └── test_service.py
│   └── integration/
│       └── test_cli.py
├── pyproject.toml
└── uv.lock
```

## Development Workflow

### 1. Create Tasks from Plan

Run `/sp.tasks` to generate implementation tasks:
```bash
# In Claude Code
/sp.tasks
```

### 2. Implement Tasks

Tasks are organized by user story priority:
- Phase 1: Setup (project structure)
- Phase 2: Foundational (models, services)
- Phase 3: User Story 1 (Add Task)
- Phase 4: User Story 2 (View Tasks)
- Phase 5: User Story 3 (Mark Complete)
- Phase 6: User Story 4 (Update Task)
- Phase 7: User Story 5 (Delete Task)

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task.py
```

### 4. Lint and Format

```bash
# Check PEP 8 compliance
ruff check src/

# Format code
ruff format src/
```

## First Implementation Steps

1. **Create project structure**:
   ```bash
   mkdir -p src/{cli,models,services} tests/{unit,integration}
   ```

2. **Create Task model** (`src/models/task.py`):
   - Define Task dataclass/dict structure
   - Add validation methods

3. **Create Task Service** (`src/services/task_service.py`):
   - Implement CRUD operations
   - Manage task list and ID counter

4. **Create CLI Menu** (`src/cli/menu.py`):
   - Implement menu display
   - Handle user input
   - Call service methods

5. **Create Entry Point** (`src/main.py`):
   - Initialize service
   - Start menu loop

## Testing Checklist

Before submitting code:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] PEP 8 compliance verified
- [ ] No [NEEDS CLARIFICATION] markers in code
- [ ] Commit message references Task ID

## Common Issues

### "Python version not found"
Ensure Python 3.13 is installed:
```bash
uv python install 3.13
```

### "Module not found"
Re-sync dependencies:
```bash
uv sync
```

### Tests not discovered
Ensure test files follow naming convention `test_*.py`:
```bash
pytest tests/ -v
```
