"""Message model for AI chatbot feature."""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class MessageRole(str, Enum):
    """Message role types following OpenAI convention."""
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(SQLModel, table=True):
    """
    A message is a single exchange in a conversation.
    Role determines the message type:
    - user: Human input
    - assistant: AI response
    - tool: Tool execution result
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False
    )
    role: str = Field(max_length=20, nullable=False)
    content: str = Field(nullable=False)
    tool_call_id: Optional[str] = Field(default=None, max_length=100)
    tool_name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
