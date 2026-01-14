"""Unit tests for the Task model."""

import pytest

from src.models.task import Task


class TestTaskInitialization:
    """Tests for Task initialization."""

    def test_create_task_with_minimal_fields(self) -> None:
        """Test creating a task with only the required title."""
        task = Task(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == "Pending"
        assert task.id == 0
        assert task.created_at is not None

    def test_create_task_with_all_fields(self) -> None:
        """Test creating a task with all fields."""
        task = Task(
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="Pending",
            id=1,
        )
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == "Pending"
        assert task.id == 1

    def test_default_status_is_pending(self) -> None:
        """Test that the default status is 'Pending'."""
        task = Task(title="Test task")
        assert task.status == "Pending"

    def test_default_description_is_empty(self) -> None:
        """Test that the default description is empty."""
        task = Task(title="Test task")
        assert task.description == ""


class TestTaskValidation:
    """Tests for Task validation."""

    def test_empty_title_raises_error(self) -> None:
        """Test that an empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_whitespace_only_title_raises_error(self) -> None:
        """Test that a whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="   ")

    def test_title_too_long_raises_error(self) -> None:
        """Test that a title over 200 characters raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Task title must be 200 characters or less"):
            Task(title=long_title)

    def test_description_too_long_raises_error(self) -> None:
        """Test that a description over 1000 characters raises ValueError."""
        long_description = "a" * 1001
        with pytest.raises(ValueError, match="Task description must be 1000 characters or less"):
            Task(title="Test task", description=long_description)

    def test_invalid_status_raises_error(self) -> None:
        """Test that an invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Task status must be 'Pending' or 'Completed'"):
            Task(title="Test task", status="Invalid")


class TestTaskMethods:
    """Tests for Task methods."""

    def test_mark_complete(self) -> None:
        """Test marking a task as complete."""
        task = Task(title="Test task")
        assert task.status == "Pending"
        task.mark_complete()
        assert task.status == "Completed"

    def test_is_complete_when_pending(self) -> None:
        """Test is_complete returns False for pending task."""
        task = Task(title="Test task")
        assert task.is_complete() is False

    def test_is_complete_when_completed(self) -> None:
        """Test is_complete returns True for completed task."""
        task = Task(title="Test task")
        task.mark_complete()
        assert task.is_complete() is True


class TestTaskSerialization:
    """Tests for Task serialization."""

    def test_to_dict(self) -> None:
        """Test converting a task to a dictionary."""
        task = Task(
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="Pending",
            id=1,
        )
        task_dict = task.to_dict()
        assert task_dict["id"] == 1
        assert task_dict["title"] == "Buy groceries"
        assert task_dict["description"] == "Milk, eggs, bread"
        assert task_dict["status"] == "Pending"
        assert "created_at" in task_dict

    def test_from_dict(self) -> None:
        """Test creating a task from a dictionary."""
        data = {
            "id": 5,
            "title": "Test task",
            "description": "A test description",
            "status": "Completed",
            "created_at": "2026-01-15T14:30:00",
        }
        task = Task.from_dict(data)
        assert task.id == 5
        assert task.title == "Test task"
        assert task.description == "A test description"
        assert task.status == "Completed"
        assert task.created_at == "2026-01-15T14:30:00"

    def test_from_dict_with_missing_fields(self) -> None:
        """Test creating a task from a dictionary with missing fields."""
        data = {"id": 1, "title": "Test task"}
        task = Task.from_dict(data)
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == ""
        assert task.status == "Pending"
