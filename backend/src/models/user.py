"""
User SQLModel entity per ADR-003 data model.
Represents authenticated users with email/password authentication.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .task import Task


class User(SQLModel, table=True):
    """
    User entity for authentication and task ownership.

    Attributes:
        id: Auto-incrementing primary key
        email: Unique email address (indexed for fast login queries)
        hashed_password: Bcrypt-hashed password (never store plaintext)
        created_at: Account creation timestamp
        tasks: Relationship to user's tasks (cascade delete)
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: User has many Tasks
    # Cascade delete: when user deleted, all tasks deleted
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

