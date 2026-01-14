"""Unit tests for the TaskService."""

import pytest

from src.services.task_service import (
    TaskAlreadyCompleteError,
    TaskNotFoundError,
    TaskService,
)


class TestTaskServiceInitialization:
    """Tests for TaskService initialization."""

    def test_initial_state_is_empty(self) -> None:
        """Test that a new TaskService has no tasks."""
        service = TaskService()
        assert service.get_task_count() == 0

    def test_initial_id_counter_starts_at_one(self) -> None:
        """Test that the ID counter starts at 1."""
        service = TaskService()
        task = service.add_task("First task")
        assert task.id == 1


class TestTaskServiceAddTask:
    """Tests for adding tasks."""

    def test_add_task_with_title_only(self) -> None:
        """Test adding a task with only a title."""
        service = TaskService()
        task = service.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == "Pending"
        assert service.get_task_count() == 1

    def test_add_task_with_title_and_description(self) -> None:
        """Test adding a task with title and description."""
        service = TaskService()
        task = service.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert service.get_task_count() == 1

    def test_add_multiple_tasks_increments_ids(self) -> None:
        """Test that adding multiple tasks gives unique IDs."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_title_raises_error(self) -> None:
        """Test that adding a task with empty title raises ValueError."""
        service = TaskService()
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")


class TestTaskServiceGetAllTasks:
    """Tests for retrieving all tasks."""

    def test_get_all_tasks_empty(self) -> None:
        """Test getting all tasks when empty."""
        service = TaskService()
        assert service.get_all_tasks() == []

    def test_get_all_tasks_returns_copy(self) -> None:
        """Test that get_all_tasks returns a copy of the list."""
        service = TaskService()
        service.add_task("Task 1")
        tasks = service.get_all_tasks()
        tasks.clear()  # This should not affect the service
        assert service.get_task_count() == 1


class TestTaskServiceGetTaskById:
    """Tests for retrieving a task by ID."""

    def test_get_task_by_id_exists(self) -> None:
        """Test getting an existing task by ID."""
        service = TaskService()
        service.add_task("Task 1")
        task = service.get_task_by_id(1)
        assert task.title == "Task 1"

    def test_get_task_by_id_not_found(self) -> None:
        """Test getting a non-existent task raises error."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.get_task_by_id(999)


class TestTaskServiceUpdateTask:
    """Tests for updating tasks."""

    def test_update_title(self) -> None:
        """Test updating only the title."""
        service = TaskService()
        service.add_task("Original title")
        task = service.update_task(1, title="New title")

        assert task.title == "New title"
        assert task.description == ""

    def test_update_description(self) -> None:
        """Test updating only the description."""
        service = TaskService()
        service.add_task("Task title")
        task = service.update_task(1, description="New description")

        assert task.title == "Task title"
        assert task.description == "New description"

    def test_update_both_title_and_description(self) -> None:
        """Test updating both title and description."""
        service = TaskService()
        service.add_task("Original", "Original description")
        task = service.update_task(1, title="New", description="New description")

        assert task.title == "New"
        assert task.description == "New description"

    def test_update_preserves_unmodified_fields(self) -> None:
        """Test that updating one field preserves the other."""
        service = TaskService()
        service.add_task("Title", "Description")
        service.update_task(1, title="New Title")
        task = service.get_task_by_id(1)

        assert task.title == "New Title"
        assert task.description == "Description"

    def test_update_empty_title_raises_error(self) -> None:
        """Test that updating with empty title raises ValueError."""
        service = TaskService()
        service.add_task("Task")
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(1, title="")

    def test_update_nonexistent_task_raises_error(self) -> None:
        """Test that updating a non-existent task raises error."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.update_task(999, title="New title")


class TestTaskServiceMarkComplete:
    """Tests for marking tasks as complete."""

    def test_mark_complete(self) -> None:
        """Test marking a pending task as complete."""
        service = TaskService()
        service.add_task("Task")
        task = service.mark_complete(1)

        assert task.status == "Completed"

    def test_mark_already_complete_raises_error(self) -> None:
        """Test that marking an already complete task raises error."""
        service = TaskService()
        service.add_task("Task")
        service.mark_complete(1)
        with pytest.raises(TaskAlreadyCompleteError):
            service.mark_complete(1)

    def test_mark_complete_nonexistent_raises_error(self) -> None:
        """Test that marking a non-existent task raises error."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.mark_complete(999)


class TestTaskServiceDeleteTask:
    """Tests for deleting tasks."""

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        assert service.get_task_count() == 2

        service.delete_task(1)
        assert service.get_task_count() == 1
        tasks = service.get_all_tasks()
        assert tasks[0].id == 2

    def test_delete_nonexistent_task_raises_error(self) -> None:
        """Test that deleting a non-existent task raises error."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)


class TestTaskServiceHelperMethods:
    """Tests for helper methods."""

    def test_get_task_count(self) -> None:
        """Test getting the task count."""
        service = TaskService()
        assert service.get_task_count() == 0

        service.add_task("Task 1")
        assert service.get_task_count() == 1

        service.add_task("Task 2")
        assert service.get_task_count() == 2

    def test_clear_all_tasks(self) -> None:
        """Test clearing all tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        assert service.get_task_count() == 2

        service.clear_all_tasks()
        assert service.get_task_count() == 0

        # Verify ID counter resets
        new_task = service.add_task("New task")
        assert new_task.id == 1
