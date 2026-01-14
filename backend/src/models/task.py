"""
Task SQLModel entity per ADR-003 data model.
Represents user-scoped todo tasks with CRUD operations.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    """
    Task entity for user-scoped todo items.

    Attributes:
        id: Auto-incrementing primary key
        title: Task title (max 200 chars)
        description: Optional detailed description (max 2000 chars)
        is_complete: Completion status (default: False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
        user_id: Foreign key to users.id (indexed for user-scoped queries)
        user: Relationship to task owner
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key with index (CRITICAL for user-scoped queries per ADR-003)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Relationship: Task belongs to User
    user: "User" = Relationship(back_populates="tasks")

