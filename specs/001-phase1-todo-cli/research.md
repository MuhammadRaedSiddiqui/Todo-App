# Research: Phase 1 In-Memory Todo CLI

## Task Storage Structure

**Decision**: Use Python list of dictionaries

**Rationale**:
- Simple and intuitive for CRUD operations
- Maintains insertion order (Python 3.7+)
- Auto-incrementing IDs achieved by tracking `len(tasks)` or `max_id + 1`
- Easy to migrate to database in Phase 2 - just replace list with DB queries
- No external dependencies required

**Alternatives Considered**:
- Dictionary keyed by ID: Rejected because list is more natural for ordered display
- Custom class with methods: Over-engineered for Phase 1 scope
- SQLite: Violates Phase 1 in-memory constraint

## CLI Interface Pattern

**Decision**: Numbered menu loop using `input()` function

**Rationale**:
- Familiar pattern for CLI applications
- Works consistently across Windows, Linux, and macOS
- Uses only Python standard library (no external dependencies)
- Clear error messages for invalid inputs

**Implementation Pattern**:
```python
while True:
    print_menu()
    choice = input("Enter choice: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    # ...
    elif choice == "6":
        break
```

**Alternatives Considered**:
- `argparse` module: Rejected - better for command-line arguments, not interactive menus
- `click` library: External dependency, unnecessary for simple menu
- `sys.stdin` directly: More complex, less readable

## Input Validation

**Decision**: Simple string validation with clear error messages

**Validation Rules**:
- Title must not be empty after strip()
- Title length reasonable (e.g., 1-200 characters)
- Description optional, accepts any string
- Menu choices validated as integers 1-6

**Error Messages**:
- Empty title: "Error: Task title cannot be empty. Please enter a valid title."
- Invalid menu choice: "Invalid choice. Please enter a number from 1 to 6."
- Invalid task ID: "Error: Task with ID {id} not found."

## Timestamp Format

**Decision**: ISO 8601 format using `datetime.now().isoformat()`

**Rationale**:
- Human-readable in display
- Standard format across systems
- Easy to sort chronologically
- Can be parsed easily if Phase 2 needs date operations

**Example Output**: "2026-01-15T14:30:00.123456"

## Task ID Generation

**Decision**: Auto-incrementing integer using counter variable

**Implementation**:
- Maintain `next_task_id` counter initialized to 1
- Increment after each task creation
- IDs never reused during session
- IDs reset on application restart (per spec assumptions)

## Error Handling Strategy

**Decision**: Graceful degradation with user-friendly messages

**Error Types and Responses**:
1. Invalid menu choice: Display menu again, ask for valid input
2. Invalid task ID: Show error, return to menu
3. Empty title: Prompt again until valid input
4. Keyboard interrupt: Clean exit with "Goodbye!"

**Key Principle**: Application never crashes on user input errors (FR-008)
