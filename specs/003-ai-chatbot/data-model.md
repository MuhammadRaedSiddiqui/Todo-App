# Data Model: AI Chatbot

**Feature**: AI Chatbot for Todo Management
**Date**: 2026-01-18
**Status**: Complete

## Overview

This document defines the database schema and data models for the AI chatbot feature. The design supports stateless conversation management with full message history persistence.

## Entity Relationship Diagram

```
User (existing from Phase 2)
  |
  | 1:N
  |
Conversation
  |
  | 1:N
  |
Message
```

## Entities

### Conversation

Represents a chat session between a user and the AI assistant.

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    A conversation is a collection of messages between a user and the AI assistant.
    Each conversation belongs to a single user and maintains chronological message history.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique conversation identifier |
| user_id | Integer | Foreign Key (users.id), NOT NULL, Indexed | Owner of the conversation |
| created_at | Timestamp | NOT NULL, Default: CURRENT_TIMESTAMP | When conversation started |
| updated_at | Timestamp | NOT NULL, Default: CURRENT_TIMESTAMP | Last message timestamp |

**Indexes**:
- Primary key on `id`
- Index on `user_id` for efficient user conversation queries
- Index on `updated_at` for sorting recent conversations

**Relationships**:
- Belongs to: User (1:1)
- Has many: Messages (1:N, cascade delete)

**Validation Rules**:
- `user_id` must reference existing user
- `created_at` cannot be in the future
- `updated_at` must be >= `created_at`

**Business Rules**:
- Each conversation is isolated to a single user
- Deleting a conversation deletes all associated messages (cascade)
- Conversations are never shared between users

---

### Message

Represents an individual message within a conversation (user input, assistant response, or tool execution).

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    """Message role types following OpenAI convention"""
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
    conversation: Conversation = Relationship(back_populates="messages")

    class Config:
        """Pydantic configuration"""
        use_enum_values = True
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique message identifier |
| conversation_id | Integer | Foreign Key (conversations.id), NOT NULL, Indexed | Parent conversation |
| role | String(20) | NOT NULL, CHECK IN ('user', 'assistant', 'tool') | Message sender type |
| content | Text | NOT NULL | Message text or tool result JSON |
| tool_call_id | String(100) | Nullable | OpenAI tool call identifier (for tool messages) |
| tool_name | String(100) | Nullable | Name of executed tool (for tool messages) |
| created_at | Timestamp | NOT NULL, Default: CURRENT_TIMESTAMP, Indexed | Message timestamp |

**Indexes**:
- Primary key on `id`
- Index on `conversation_id` for retrieving conversation history
- Index on `created_at` for chronological ordering

**Relationships**:
- Belongs to: Conversation (N:1)

**Validation Rules**:
- `role` must be one of: 'user', 'assistant', 'tool'
- `content` cannot be empty string
- If `role` is 'tool', `tool_call_id` and `tool_name` should be populated
- If `role` is 'user' or 'assistant', `tool_call_id` and `tool_name` should be NULL
- `conversation_id` must reference existing conversation

**Business Rules**:
- Messages are immutable once created (no updates)
- Messages are ordered chronologically by `created_at`
- Tool messages always follow assistant messages with tool_calls
- Message content for tool role contains JSON-serialized tool result

---

## Database Migrations

### Migration 001: Create Conversations and Messages Tables

**File**: `backend/migrations/versions/003_create_chat_tables.py`

```python
"""Create conversations and messages tables for AI chatbot

Revision ID: 003
Revises: 002
Create Date: 2026-01-18
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003'
down_revision = '002'  # Previous migration from Phase 2
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_call_id', sa.String(length=100), nullable=True),
        sa.Column('tool_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("role IN ('user', 'assistant', 'tool')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_updated_at', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
```

---

## Data Access Patterns

### Common Queries

**1. Get all conversations for a user (most recent first)**:

```python
from sqlmodel import select

conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
).all()
```

**2. Get conversation with all messages**:

```python
conversation = session.exec(
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .where(Conversation.user_id == user_id)  # Security: verify ownership
).first()

if conversation:
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    ).all()
```

**3. Create new conversation with initial message**:

```python
# Create conversation
conversation = Conversation(user_id=user_id)
session.add(conversation)
session.commit()
session.refresh(conversation)

# Add first message
message = Message(
    conversation_id=conversation.id,
    role="user",
    content=user_input
)
session.add(message)
session.commit()
```

**4. Append message to existing conversation**:

```python
message = Message(
    conversation_id=conversation_id,
    role=role,
    content=content,
    tool_call_id=tool_call_id,  # Optional
    tool_name=tool_name  # Optional
)
session.add(message)

# Update conversation timestamp
conversation.updated_at = datetime.utcnow()
session.add(conversation)
session.commit()
```

---

## Storage Estimates

**Assumptions**:
- Average conversation: 20 messages
- Average message length: 200 characters
- 1000 active users
- Each user has 5 conversations on average

**Calculations**:

```
Conversations:
- 1000 users × 5 conversations = 5,000 rows
- Row size: ~50 bytes
- Total: 250 KB

Messages:
- 5,000 conversations × 20 messages = 100,000 rows
- Row size: ~300 bytes (including content)
- Total: 30 MB

Indexes:
- Estimated 20% overhead: 6 MB

Total Storage: ~36 MB for 1000 users
```

**Scaling**: At 100K users, estimated storage is ~3.6 GB, well within PostgreSQL capacity.

---

## Data Retention Policy

**Current Policy**: Indefinite retention

**Future Considerations**:
- Archive conversations older than 90 days
- Delete conversations with no messages
- Implement user-initiated conversation deletion
- Add soft delete flag for audit trail

---

## Security Considerations

1. **User Isolation**: All queries MUST filter by `user_id` to prevent cross-user data access
2. **Conversation Ownership**: Verify conversation belongs to authenticated user before operations
3. **Content Sanitization**: Sanitize message content before storage to prevent XSS
4. **Tool Call Validation**: Validate tool execution results before storing in messages
5. **Rate Limiting**: Limit message creation rate per user to prevent abuse

---

## Testing Strategy

**Unit Tests**:
- Model validation (field constraints, enums)
- Relationship integrity (cascade deletes)
- Timestamp defaults and updates

**Integration Tests**:
- Create conversation with messages
- Retrieve conversation history
- Delete conversation (verify cascade)
- Query performance with large datasets

**Contract Tests**:
- Verify database schema matches SQLModel definitions
- Validate migration up/down operations
