"""Task model for the Todo CLI application."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a single to-do item.

    Attributes:
        id: Unique integer identifier (auto-assigned on creation)
        title: Task title (required, 1-200 characters)
        description: Optional task description (0-1000 characters)
        status: Task status, either "Pending" or "Completed"
        created_at: ISO 8601 timestamp when task was created
    """

    title: str
    description: str = ""
    status: str = "Pending"
    id: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        self._validate_title()
        self._validate_description()
        self._validate_status()

    def _validate_title(self) -> None:
        """Validate that title is not empty and within length limits."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Task title must be 200 characters or less")

    def _validate_description(self) -> None:
        """Validate that description is within length limits."""
        if len(self.description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")

    def _validate_status(self) -> None:
        """Validate that status is a valid value."""
        if self.status not in ("Pending", "Completed"):
            raise ValueError("Task status must be 'Pending' or 'Completed'")

    def to_dict(self) -> dict:
        """Convert task to dictionary for in-memory storage.

        Returns:
            Dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing task data.

        Returns:
            New Task instance.
        """
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.status = "Completed"

    def is_complete(self) -> bool:
        """Check if the task is completed.

        Returns:
            True if status is "Completed", False otherwise.
        """
        return self.status == "Completed"
