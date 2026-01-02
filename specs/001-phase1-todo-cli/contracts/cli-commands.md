# CLI Contracts: Phase 1 In-Memory Todo CLI

## Main Menu Interface

### Menu Display

```
=== TODO LIST MENU ===
1. Add Task
2. View Tasks
3. Update Task
4. Mark Complete
5. Delete Task
6. Exit

Enter your choice (1-6):
```

### Menu Options

| Option | Action | User Input Required |
|--------|--------|---------------------|
| 1 | Add Task | Title (required), Description (optional) |
| 2 | View Tasks | None |
| 3 | Update Task | Task ID, New Title (optional), New Description (optional) |
| 4 | Mark Complete | Task ID |
| 5 | Delete Task | Task ID, Confirmation (Y/N) |
| 6 | Exit | None |

## Command Contracts

### 1. Add Task

**Trigger**: User selects menu option 1

**User Input Flow**:
```
1. System displays: "Enter task title:"
2. User enters title
3. If empty: Display error, repeat step 2
4. System displays: "Enter task description (optional):"
5. User enters description (or presses Enter to skip)
6. System creates task and displays confirmation
```

**Success Output**:
```
Task added successfully! (ID: 1)
```

**Error States**:
- Empty title: "Error: Task title cannot be empty. Please enter a valid title."

---

### 2. View Tasks

**Trigger**: User selects menu option 2

**Display Format**:
```
=== YOUR TASKS ===
ID | Status     | Title
--------------------
1  | Pending    | Buy groceries
2  | Completed  | Call mom
3  | Pending    | Finish report

(3 tasks total)
```

**Empty State**:
```
No tasks yet. Add your first task!
```

---

### 3. Update Task

**Trigger**: User selects menu option 3

**User Input Flow**:
```
1. System displays: "Enter task ID to update:"
2. User enters ID
3. If invalid: Display error, return to menu
4. System shows current task details
5. System displays: "Enter new title (or press Enter to keep current):"
6. User enters new title or presses Enter
7. System displays: "Enter new description (or press Enter to keep current):"
8. User enters new description or presses Enter
9. System updates and confirms
```

**Success Output**:
```
Task 1 updated successfully!
```

**Error States**:
- Invalid ID: "Error: Task with ID 5 not found."

---

### 4. Mark Complete

**Trigger**: User selects menu option 4

**User Input Flow**:
```
1. System displays: "Enter task ID to mark as complete:"
2. User enters ID
3. If invalid: Display error, return to menu
4. System updates status and confirms
```

**Success Output**:
```
Task 1 marked as complete!
```

**Error States**:
- Invalid ID: "Error: Task with ID 5 not found."
- Already complete: "Task 2 is already marked as complete."

---

### 5. Delete Task

**Trigger**: User selects menu option 5

**User Input Flow**:
```
1. System displays: "Enter task ID to delete:"
2. User enters ID
3. If invalid: Display error, return to menu
4. System displays: "Are you sure you want to delete 'Buy groceries'? (y/n):"
5. User enters 'y' or 'n'
6. If 'y': Delete task and confirm
7. If 'n': Cancel and return to menu
```

**Success Output**:
```
Task deleted successfully!
```

**Error States**:
- Invalid ID: "Error: Task with ID 5 not found."

---

### 6. Exit

**Trigger**: User selects menu option 6

**Output**:
```
Goodbye! Thanks for using Todo List.
```

**Behavior**: Application terminates

## Input Specifications

### Valid Task ID
- Positive integer
- Must exist in task list
- Example: `1`, `2`, `15`

### Valid Menu Choice
- Integer 1-6
- No decimals or other characters
- Example: `1`, `2`, `3`, `4`, `5`, `6`

### Valid Title
- 1-200 characters
- Not empty after strip()
- All characters allowed
- Example: "Buy groceries", "Task #123"

### Valid Description (Optional)
- 0-1000 characters
- Empty string allowed (user presses Enter)
- All characters allowed
- Example: "Milk, eggs, bread", ""

## Error Message Standards

All error messages follow this format:
```
Error: [Descriptive message explaining what went wrong]
```

Common errors:
- Invalid menu choice: "Error: Invalid choice. Please enter a number from 1 to 6."
- Invalid task ID: "Error: Task with ID {id} not found."
- Empty title: "Error: Task title cannot be empty."
- Already complete: "Task {id} is already marked as complete."
- Delete cancelled: "Delete cancelled."
