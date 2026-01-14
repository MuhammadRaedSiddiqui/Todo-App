"""
Task API endpoints.
Implements RESTful CRUD operations per contracts/api-spec.yaml.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from src.api.dependencies import get_current_user
from src.core.database import get_session
from src.models.user import User
from src.services import task_service

# Request/Response models per contracts/api-spec.yaml

class TaskCreate(BaseModel):
    """Request body for creating a task."""
    title: str = Field(..., max_length=200, description="Task title (required)")
    description: Optional[str] = Field(
        None, max_length=2000, description="Task description (optional)"
    )


class TaskUpdate(BaseModel):
    """Request body for updating a task."""
    title: Optional[str] = Field(None, max_length=200, description="Updated title")
    description: Optional[str] = Field(None, max_length=2000, description="Updated description")


class TaskComplete(BaseModel):
    """Request body for toggling task completion."""
    is_complete: bool = Field(..., description="Completion status")


class TaskResponse(BaseModel):
    """Response body for task operations."""
    id: int
    title: str
    description: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True


# API Router
router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])


def verify_user_authorization(user_id: int, current_user: User):
    """
    Verify that the user_id in the path matches the authenticated user.

    Implements FR-025, FR-026, FR-027.

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Cannot access other users' tasks"
        )


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for authenticated user.

    Implements FR-015, FR-014, FR-021, FR-026.

    Endpoint: GET /api/v1/users/{user_id}/tasks

    Returns:
        - 200: List of tasks (newest first)
        - 401: Unauthorized (missing/invalid JWT)
        - 403: Forbidden (user_id mismatch)
    """
    # Verify authorization (FR-025, FR-026)
    verify_user_authorization(user_id, current_user)

    # List tasks (FR-015, FR-014)
    tasks = task_service.list_user_tasks(session, user_id)

    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task.

    Implements FR-009, FR-010, FR-011, FR-026.

    Endpoint: POST /api/v1/users/{user_id}/tasks

    Request body:
        - title: Task title (required, max 200 chars)
        - description: Task description (optional, max 2000 chars)

    Returns:
        - 201: Task created successfully
        - 400: Invalid input (title/description too long)
        - 401: Unauthorized
        - 403: Forbidden (user_id mismatch)
    """
    # Verify authorization (FR-026)
    verify_user_authorization(user_id, current_user)

    try:
        # Create task (FR-009)
        task = task_service.create_task(
            session,
            user_id,
            task_data.title,
            task_data.description
        )
        return task

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a single task by ID.

    Implements FR-016, FR-022, FR-026.

    Endpoint: GET /api/v1/users/{user_id}/tasks/{task_id}

    Returns:
        - 200: Task details
        - 401: Unauthorized
        - 403: Forbidden (user_id mismatch)
        - 404: Task not found
    """
    # Verify authorization (FR-026)
    verify_user_authorization(user_id, current_user)

    # Get task with authorization check (FR-022)
    task = task_service.get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task's title and/or description.

    Implements FR-019, FR-023, FR-026.

    Endpoint: PUT /api/v1/users/{user_id}/tasks/{task_id}

    Request body:
        - title: Updated title (optional, max 200 chars)
        - description: Updated description (optional, max 2000 chars)

    Returns:
        - 200: Task updated successfully
        - 400: Invalid input
        - 401: Unauthorized
        - 403: Forbidden (user_id mismatch)
        - 404: Task not found
    """
    # Verify authorization (FR-026)
    verify_user_authorization(user_id, current_user)

    try:
        # Update task (FR-019, FR-023)
        task = task_service.update_task(
            session,
            task_id,
            user_id,
            task_data.title,
            task_data.description
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_complete(
    user_id: int,
    task_id: int,
    complete_data: TaskComplete,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Implements FR-017, FR-018, FR-026.

    Endpoint: PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete

    Request body:
        - is_complete: true to mark complete, false to mark incomplete

    Returns:
        - 200: Task completion status updated
        - 401: Unauthorized
        - 403: Forbidden (user_id mismatch)
        - 404: Task not found
    """
    # Verify authorization (FR-026)
    verify_user_authorization(user_id, current_user)

    # Toggle completion (FR-017, FR-018)
    task = task_service.toggle_task_complete(
        session,
        task_id,
        user_id,
        complete_data.is_complete
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    Implements FR-020, FR-024, FR-026.

    Endpoint: DELETE /api/v1/users/{user_id}/tasks/{task_id}

    Returns:
        - 204: Task deleted successfully
        - 401: Unauthorized
        - 403: Forbidden (user_id mismatch)
        - 404: Task not found
    """
    # Verify authorization (FR-026)
    verify_user_authorization(user_id, current_user)

    # Delete task (FR-020, FR-024)
    deleted = task_service.delete_task(session, task_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None
