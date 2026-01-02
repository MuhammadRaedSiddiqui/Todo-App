# Data Model: Phase 1 In-Memory Todo CLI

## Task Entity

### Structure

```python
{
    "id": int,
    "title": str,
    "description": str,
    "status": str,  # "Pending" or "Completed"
    "created_at": str  # ISO 8601 timestamp
}
```

### Field Definitions

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `id` | Integer | Yes | Auto-generated | Unique, auto-incrementing |
| `title` | String | Yes | N/A | 1-200 characters, non-empty |
| `description` | String | No | "" (empty string) | 0-1000 characters |
| `status` | String | No | "Pending" | Must be "Pending" or "Completed" |
| `created_at` | String | Yes | Auto-generated | ISO 8601 format |

### State Transitions

```
Created:        id assigned, status="Pending"
    ↓
Mark Complete:  status changes to "Completed"
    ↓
Deleted:        removed from task list (terminal state)
```

Note: Status can only transition from "Pending" to "Completed" (one-way for Phase 1).

## Storage Structure

### Task List

```python
tasks: List[Dict] = []
```

- Tasks stored in insertion order
- New tasks appended to end
- Display shows tasks in list order
- Delete by ID shifts remaining tasks (IDs unchanged)

### ID Counter

```python
next_task_id: int = 1
```

- Increments before assigning to new task
- Never decrements during session
- Resets when application restarts

## Example Data

### Single Task
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "created_at": "2026-01-15T14:30:00"
}
```

### Multiple Tasks
```python
[
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "status": "Pending",
        "created_at": "2026-01-15T14:30:00"
    },
    {
        "id": 2,
        "title": "Call mom",
        "description": "",
        "status": "Completed",
        "created_at": "2026-01-15T15:00:00"
    }
]
```

## Validation Rules

### Title Validation
- Must not be empty (whitespace-only rejected)
- Must be 1-200 characters
- Special characters allowed (no SQL injection risk - no database)

### Description Validation
- Optional (defaults to empty string)
- Maximum 1000 characters (reasonable limit for CLI display)
- Special characters allowed

### Status Validation
- Must be exactly "Pending" or "Completed"
- Case-sensitive (always stored with proper capitalization)

## Phase 2 Migration Notes

This data model is designed for easy migration to a database:

1. **List to Table**: `tasks` list becomes `tasks` table
2. **Dict to Row**: Each task dict becomes a table row
3. **Auto-increment**: Database sequence replaces `next_task_id`
4. **Timestamps**: `created_at` can remain string or become TIMESTAMP type
5. **Status Enum**: Can become ENUM or foreign key to status table
