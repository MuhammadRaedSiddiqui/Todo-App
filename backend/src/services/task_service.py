"""
Task service layer for CRUD operations.
Implements business logic for task management per FR-009 through FR-020.
"""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from src.models.task import Task


def create_task(
    session: Session,
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> Task:
    """
    Create a new task for a user.

    Implements FR-009, FR-010, FR-011, FR-012, FR-013.

    Args:
        session: Database session
        user_id: Owner user ID
        title: Task title (max 200 chars)
        description: Optional task description (max 2000 chars)

    Returns:
        Created Task object

    Raises:
        ValueError: If title exceeds 200 chars or description exceeds 2000 chars
    """
    # Validate title length (FR-010)
    if len(title) > 200:
        raise ValueError("Title must not exceed 200 characters")

    # Validate description length if provided (FR-011)
    if description and len(description) > 2000:
        raise ValueError("Description must not exceed 2000 characters")

    # Create task (FR-009, FR-012, FR-013)
    task = Task(
        title=title,
        description=description,
        user_id=user_id,
        is_complete=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def list_user_tasks(session: Session, user_id: int) -> List[Task]:
    """
    List all tasks for a user, ordered by creation date descending.

    Implements FR-014, FR-015, FR-021.

    Args:
        session: Database session
        user_id: User ID to filter tasks

    Returns:
        List of Task objects (newest first)
    """
    # Query tasks filtered by user_id with index (FR-021)
    # Order by created_at DESC (FR-014)
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )

    tasks = session.exec(statement).all()
    return list(tasks)


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a single task by ID with user authorization check.

    Implements FR-016, FR-022.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for authorization

    Returns:
        Task object if found and authorized, None otherwise
    """
    # Query with both task_id and user_id for authorization (FR-022)
    statement = (
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    )

    task = session.exec(statement).first()
    return task


def update_task(
    session: Session,
    task_id: int,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    """
    Update a task's title and/or description.

    Implements FR-019, FR-023.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for authorization
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated Task object if found and authorized, None otherwise

    Raises:
        ValueError: If title exceeds 200 chars or description exceeds 2000 chars
    """
    # Get task with authorization check (FR-023)
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Validate and update title if provided (FR-010)
    if title is not None:
        if len(title) > 200:
            raise ValueError("Title must not exceed 200 characters")
        task.title = title

    # Validate and update description if provided (FR-011)
    if description is not None:
        if len(description) > 2000:
            raise ValueError("Description must not exceed 2000 characters")
        task.description = description

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def toggle_task_complete(
    session: Session,
    task_id: int,
    user_id: int,
    is_complete: bool
) -> Optional[Task]:
    """
    Toggle task completion status.

    Implements FR-017, FR-018.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for authorization
        is_complete: New completion status

    Returns:
        Updated Task object if found and authorized, None otherwise
    """
    # Get task with authorization check
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Update completion status (FR-017, FR-018)
    task.is_complete = is_complete
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task permanently.

    Implements FR-020, FR-024.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for authorization

    Returns:
        True if task was deleted, False if not found or unauthorized
    """
    # Get task with authorization check (FR-024)
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    # Delete task (FR-020)
    session.delete(task)
    session.commit()

    return True
