"""Integration tests for CLI workflows."""

import pytest

from src.cli.menu import TodoMenu
from src.services.task_service import TaskService


class TestCLIWorkflows:
    """Integration tests for complete CLI workflows."""

    @pytest.fixture
    def service(self) -> TaskService:
        """Create a fresh TaskService for each test."""
        return TaskService()

    @pytest.fixture
    def menu(self, service: TaskService) -> TodoMenu:
        """Create a TodoMenu with the service."""
        return TodoMenu(service)

    def test_add_and_view_task(self, service: TaskService) -> None:
        """Test adding a task and viewing it."""
        task = service.add_task("Buy groceries", "Milk, eggs, bread")
        assert task.id == 1
        assert task.status == "Pending"

        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    def test_complete_task_workflow(self, service: TaskService) -> None:
        """Test the complete task lifecycle."""
        # Add task
        task = service.add_task("Test task")
        assert task.id == 1
        assert not task.is_complete()

        # Mark complete
        completed_task = service.mark_complete(1)
        assert completed_task.is_complete()

        # View all
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].status == "Completed"

    def test_update_task_workflow(self, service: TaskService) -> None:
        """Test updating a task."""
        service.add_task("Original title", "Original description")

        # Update title
        updated = service.update_task(1, title="New title")
        assert updated.title == "New title"
        assert updated.description == "Original description"

        # Update description
        updated = service.update_task(1, description="New description")
        assert updated.description == "New description"

    def test_delete_task_workflow(self, service: TaskService) -> None:
        """Test deleting a task."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        assert service.get_task_count() == 2

        service.delete_task(1)
        assert service.get_task_count() == 1

        # Verify remaining task is task 2
        tasks = service.get_all_tasks()
        assert tasks[0].id == 2

    def test_get_nonexistent_task_raises_error(self, service: TaskService) -> None:
        """Test that getting a non-existent task raises an error."""
        from src.services.task_service import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            service.get_task_by_id(999)

    def test_delete_nonexistent_task_raises_error(self, service: TaskService) -> None:
        """Test that deleting a non-existent task raises an error."""
        from src.services.task_service import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)

    def test_mark_already_complete_task_raises_error(self, service: TaskService) -> None:
        """Test that marking an already complete task raises an error."""
        from src.services.task_service import TaskAlreadyCompleteError

        service.add_task("Task")
        service.mark_complete(1)

        with pytest.raises(TaskAlreadyCompleteError):
            service.mark_complete(1)

    def test_update_nonexistent_task_raises_error(self, service: TaskService) -> None:
        """Test that updating a non-existent task raises an error."""
        from src.services.task_service import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            service.update_task(999, title="New title")

    def test_update_with_empty_title_raises_error(self, service: TaskService) -> None:
        """Test that updating with an empty title raises an error."""
        service.add_task("Task")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(1, title="")

    def test_add_empty_title_raises_error(self, service: TaskService) -> None:
        """Test that adding a task with empty title raises an error."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")

    def test_clear_all_tasks(self, service: TaskService) -> None:
        """Test clearing all tasks."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        assert service.get_task_count() == 2

        service.clear_all_tasks()
        assert service.get_task_count() == 0

        # Verify ID counter resets
        task = service.add_task("New task")
        assert task.id == 1


class TestInputValidation:
    """Tests for input validation in CLI."""

    @pytest.fixture
    def service(self) -> TaskService:
        """Create a fresh TaskService for each test."""
        return TaskService()

    def test_title_length_limit(self, service: TaskService) -> None:
        """Test that title is limited to 200 characters."""
        long_title = "a" * 200
        task = service.add_task(long_title)
        assert len(task.title) == 200

        with pytest.raises(ValueError):
            service.add_task("a" * 201)

    def test_description_length_limit(self, service: TaskService) -> None:
        """Test that description is limited to 1000 characters."""
        long_description = "a" * 1000
        task = service.add_task("Task", long_description)
        assert len(task.description) == 1000

    def test_invalid_status_rejected(self) -> None:
        """Test that invalid status is rejected."""
        from src.models.task import Task

        with pytest.raises(ValueError, match="Task status must be 'Pending' or 'Completed'"):
            Task(title="Task", status="Invalid")
