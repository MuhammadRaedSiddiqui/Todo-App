"""
SQLModel entities export.
Import all models here to ensure they're registered with SQLModel metadata.
"""

from .task import Task
from .user import User

__all__ = ["User", "Task"]
