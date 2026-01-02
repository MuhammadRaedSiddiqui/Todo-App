"""TaskService for managing todo tasks with in-memory storage."""

from typing import Optional

from src.models.task import Task


class TaskServiceError(Exception):
    """Base exception for task service errors."""

    pass


class TaskNotFoundError(TaskServiceError):
    """Raised when a task with the given ID is not found."""

    pass


class TaskAlreadyCompleteError(TaskServiceError):
    """Raised when trying to complete an already completed task."""

    pass


class TaskService:
    """Service for managing tasks with in-memory storage.

    Attributes:
        tasks: List of Task objects stored in memory.
        next_task_id: Counter for generating unique task IDs.
    """

    def __init__(self) -> None:
        """Initialize the task service with empty storage."""
        self._tasks: list[Task] = []
        self._next_task_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task with the given title and description.

        Args:
            title: The task title (required).
            description: Optional task description.

        Returns:
            The newly created Task.

        Raises:
            ValueError: If title is empty or invalid.
        """
        task = Task(title=title, description=description)
        task.id = self._next_task_id
        self._next_task_id += 1
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all tasks in insertion order.
        """
        return list(self._tasks)

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task with the given ID.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional, keeps current if not provided).
            description: New description (optional, keeps current if not provided).

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            ValueError: If title is empty when provided.
        """
        task = self.get_task_by_id(task_id)

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        return task

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed.

        Args:
            task_id: The ID of the task to mark as complete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            TaskAlreadyCompleteError: If task is already completed.
        """
        task = self.get_task_by_id(task_id)

        if task.is_complete():
            raise TaskAlreadyCompleteError(f"Task {task_id} is already completed")

        task.mark_complete()
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        task = self.get_task_by_id(task_id)
        self._tasks.remove(task)

    def get_task_count(self) -> int:
        """Get the total number of tasks.

        Returns:
            Number of tasks in storage.
        """
        return len(self._tasks)

    def clear_all_tasks(self) -> None:
        """Remove all tasks from storage and reset ID counter.

        Note: This is primarily useful for testing.
        """
        self._tasks.clear()
        self._next_task_id = 1
