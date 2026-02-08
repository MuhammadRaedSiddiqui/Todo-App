"""MCP tool definitions for task operations."""
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select
from src.models.task import Task


# Tool Schemas (OpenAI Function Calling Format)

ADD_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new todo task for the authenticated user. Use this when the user wants to add, create, or remember something to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title or description. Should be clear and concise.",
                },
                "due_date": {
                    "type": "string",
                    "description": "Optional due date in ISO 8601 format (YYYY-MM-DD). Parse natural language dates like 'tomorrow', 'next Monday', 'in 3 days' into ISO format.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Task priority level. Default to 'medium' if not specified by user.",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional additional notes or details about the task",
                }
            },
            "required": ["title"]
        }
    }
}

LIST_TASKS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Retrieve all tasks for the authenticated user. Use this when the user wants to see, view, or check their tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed", "all"],
                    "description": "Filter tasks by completion status. 'pending' shows incomplete tasks, 'completed' shows finished tasks, 'all' shows everything.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Optional filter by priority level",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return",
                }
            },
            "required": []
        }
    }
}

UPDATE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update an existing task. Use this when the user wants to modify, change, edit, or mark a task as complete/incomplete.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The unique identifier of the task to update. Must be a task owned by the authenticated user.",
                },
                "title": {
                    "type": "string",
                    "description": "New task title (optional)",
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed"],
                    "description": "New task status. Use 'completed' to mark as done, 'pending' to mark as incomplete.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "New priority level (optional)",
                },
                "due_date": {
                    "type": "string",
                    "description": "New due date in ISO 8601 format (YYYY-MM-DD), or null to remove due date",
                },
                "notes": {
                    "type": "string",
                    "description": "New notes (optional)",
                }
            },
            "required": ["task_id"]
        }
    }
}

DELETE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a task permanently. Use this when the user wants to remove, delete, or get rid of a task. Always confirm with the user before calling this function.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The unique identifier of the task to delete. Must be a task owned by the authenticated user.",
                }
            },
            "required": ["task_id"]
        }
    }
}

GET_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_task",
        "description": "Retrieve details of a specific task by ID. Use this when the user references a specific task and you need more information about it.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The unique identifier of the task to retrieve",
                }
            },
            "required": ["task_id"]
        }
    }
}


# Tool Execution Functions

def add_task(
    title: str,
    user_id: int,
    session: Session,
    due_date: Optional[str] = None,
    priority: str = "medium",
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        title: Task title
        user_id: ID of the authenticated user
        session: Database session
        due_date: Optional due date (ISO format)
        priority: Task priority (low/medium/high)
        notes: Optional notes

    Returns:
        Dictionary with task_id and status
    """
    task = Task(
        title=title,
        user_id=user_id,
        description=notes,  # Map notes to description field
        completed=False,
        priority=priority
    )

    if due_date:
        try:
            task.due_date = datetime.fromisoformat(due_date)
        except ValueError:
            pass  # Invalid date format, skip

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "title": task.title,
        "status": "created"
    }


def list_tasks(
    user_id: int,
    session: Session,
    status: str = "all",
    priority: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    List tasks for the user.

    Args:
        user_id: ID of the authenticated user
        session: Database session
        status: Filter by status (pending/completed/all)
        priority: Optional filter by priority
        limit: Maximum number of tasks to return

    Returns:
        Dictionary with tasks list and total count
    """
    query = select(Task).where(Task.user_id == user_id)

    # Map status filter to completed field
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    # "all" means no filter

    if priority:
        query = query.where(Task.priority == priority)

    query = query.limit(limit)

    tasks = session.exec(query).all()

    return {
        "tasks": [
            {
                "task_id": task.id,
                "title": task.title,
                "status": "completed" if task.completed else "pending",
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ],
        "total": len(tasks)
    }


def update_task(
    task_id: int,
    user_id: int,
    session: Session,
    title: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing task.

    Args:
        task_id: ID of the task to update
        user_id: ID of the authenticated user
        session: Database session
        title: New title (optional)
        status: New status (optional)
        priority: New priority (optional)
        due_date: New due date (optional)
        notes: New notes (optional)

    Returns:
        Dictionary with task_id, status, and changes

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise ValueError(f"Task {task_id} not found or access denied")

    changes = {}

    if title is not None:
        task.title = title
        changes["title"] = title

    if status is not None:
        # Map status string to completed boolean
        if status == "completed":
            task.completed = True
            changes["status"] = "completed"
        elif status == "pending":
            task.completed = False
            changes["status"] = "pending"

    if priority is not None:
        task.priority = priority
        changes["priority"] = priority

    if due_date is not None:
        try:
            task.due_date = datetime.fromisoformat(due_date)
            changes["due_date"] = due_date
        except ValueError:
            pass

    if notes is not None:
        task.description = notes  # Map notes to description field
        changes["notes"] = notes

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()

    return {
        "task_id": task_id,
        "status": "updated",
        "changes": changes
    }


def delete_task(
    task_id: int,
    user_id: int,
    session: Session
) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        Dictionary with task_id and status

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise ValueError(f"Task {task_id} not found or access denied")

    session.delete(task)
    session.commit()

    return {
        "task_id": task_id,
        "status": "deleted"
    }


def get_task(
    task_id: int,
    user_id: int,
    session: Session
) -> Dict[str, Any]:
    """
    Get details of a specific task.

    Args:
        task_id: ID of the task to retrieve
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        Dictionary with task details

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        raise ValueError(f"Task {task_id} not found or access denied")

    return {
        "task_id": task.id,
        "title": task.title,
        "status": "completed" if task.completed else "pending",
        "priority": task.priority,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "notes": task.description,  # Map description to notes
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


# Export all schemas
ALL_TOOL_SCHEMAS = [
    ADD_TASK_SCHEMA,
    LIST_TASKS_SCHEMA,
    UPDATE_TASK_SCHEMA,
    DELETE_TASK_SCHEMA,
    GET_TASK_SCHEMA
]
