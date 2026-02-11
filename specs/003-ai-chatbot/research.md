# Research: AI Chatbot Technical Implementation

**Feature**: AI Chatbot for Todo Management
**Date**: 2026-01-18
**Status**: Complete

## Overview

This document captures technical research and decisions for implementing an AI-powered chatbot using Groq's Llama 3.3 model with OpenAI SDK compatibility pattern.

## Research Areas

### 1. Groq Integration with OpenAI SDK Compatibility

**Decision**: Use OpenAI Python SDK with custom `base_url` to connect to Groq API

**Implementation Pattern**:

```python
from openai import OpenAI

# Initialize client with Groq endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Model constant
MODEL = "llama-3.3-70b-versatile"

# Usage (identical to OpenAI API)
response = client.chat.completions.create(
    model=MODEL,
    messages=[...],
    tools=[...],  # Tool calling supported
    temperature=0.7
)
```

**Rationale**:
- Groq provides OpenAI-compatible API endpoints, enabling drop-in replacement
- No need for custom SDK or API client implementation
- Standard OpenAI SDK patterns work without modification
- Tool calling (function calling) is fully supported by Groq

**Alternatives Considered**:
- **Custom HTTP client**: Rejected - unnecessary complexity, reinventing the wheel
- **Groq-specific SDK**: Rejected - doesn't exist, would require maintenance
- **LangChain integration**: Rejected - adds unnecessary abstraction layer for our use case

**Key Constraints**:
- Must NOT use OpenAI Assistants API (incompatible with Groq)
- Must use Chat Completions API with tool calling
- Rate limits: Groq free tier allows ~30 requests/minute
- Context window: ~8K tokens for Llama 3.3

---

### 2. Tool Calling Schema (MCP Pattern)

**Decision**: Define tools using OpenAI function calling schema format

**Tool Schema Structure**:

```python
# Tool definition format (OpenAI/Groq compatible)
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new todo task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title or description"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in ISO format (YYYY-MM-DD)",
                        "nullable": True
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority level"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve all tasks for the authenticated user",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed", "all"],
                        "description": "Filter tasks by status"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title",
                        "nullable": True
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "New task status",
                        "nullable": True
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO format",
                        "nullable": True
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]
```

**Rationale**:
- OpenAI function calling format is industry standard
- Groq fully supports this schema format
- Clear parameter types and descriptions improve AI accuracy
- Enum constraints prevent invalid values

**Tool Execution Flow**:
1. User sends message → Backend retrieves conversation history
2. Backend calls Groq with messages + tool definitions
3. If Groq returns `tool_calls`, execute corresponding Python function
4. Append tool result to messages, call Groq again for final response
5. Return assistant's response to user

---

### 3. Frontend Chat Interface Strategy

**Decision**: Use Vercel AI SDK's `useChat` hook for React integration

**Implementation Approach**:

```typescript
// frontend/src/components/chat/ChatInterface.tsx
import { useChat } from 'ai/react';

export function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/message',  // Backend endpoint
    headers: {
      Authorization: `Bearer ${getJwtToken()}`
    }
  });

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput
        value={input}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
        disabled={isLoading}
      />
    </div>
  );
}
```

**Rationale**:
- Vercel AI SDK provides battle-tested chat UI patterns
- `useChat` hook handles message state, streaming, and error handling
- No need for `@openai/chatkit-react` (as specified in requirements)
- Simple `fetch` alternative available if SDK not desired

**Alternative (Simple Fetch)**:

```typescript
// If not using Vercel AI SDK
const sendMessage = async (message: string) => {
  const response = await fetch('/api/chat/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message, conversation_id })
  });

  const data = await response.json();
  setMessages([...messages, data.message]);
};
```

**UI Components**:
- `ChatInterface.tsx`: Main container with useChat hook
- `MessageList.tsx`: Scrollable message display with user/assistant distinction
- `MessageInput.tsx`: Text input with send button
- `ToolCallDisplay.tsx`: Visual indicator when AI executes tools

---

### 4. Database Schema Design

**Decision**: Two-table design for conversation history

**Schema**:

```sql
-- Conversation table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Message table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    tool_call_id VARCHAR(100),  -- For tool messages
    tool_name VARCHAR(100),     -- For tool messages
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**Rationale**:
- Conversation: Groups messages by user session
- Message: Stores individual messages with role (user/assistant/tool)
- `tool_call_id` and `tool_name`: Track tool execution for debugging
- Indexes on foreign keys and timestamps for query performance
- Cascade delete ensures cleanup when conversation deleted

**SQLModel Implementation**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user', 'assistant', 'tool'
    content: str
    tool_call_id: Optional[str] = Field(default=None, max_length=100)
    tool_name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    conversation: Conversation = Relationship(back_populates="messages")
```

---

### 5. Stateless Chat Endpoint Design

**Decision**: Retrieve full conversation history on each request

**Request Flow**:

```
1. POST /api/chat/message
   Body: { "message": "Add task to buy milk", "conversation_id": 123 }
   Headers: { "Authorization": "Bearer <jwt>" }

2. Backend:
   a. Verify JWT, extract user_id
   b. Validate conversation belongs to user
   c. Retrieve all messages for conversation_id (ordered by created_at)
   d. Append new user message to history
   e. Call Groq with full message history + tools
   f. If tool_calls returned:
      - Execute tools with user_id scope
      - Append tool results to history
      - Call Groq again for final response
   g. Save assistant response to database
   h. Return response to frontend

3. Response: { "message": "I've added 'buy milk' to your tasks.", "conversation_id": 123 }
```

**Rationale**:
- Stateless design scales horizontally (no server-side sessions)
- Database is single source of truth for conversation state
- Each request is independent and can be handled by any backend instance
- Conversation history provides context for AI responses

**Context Window Management**:
- Llama 3.3 has ~8K token limit
- If conversation exceeds limit, truncate oldest messages
- Keep system prompt + last N messages that fit in window
- Implement token counting using `tiktoken` library

---

## Best Practices

### Security
- Store Groq API key in environment variable (`GROQ_API_KEY`)
- Validate JWT on every chat request
- Scope all tool executions to authenticated user_id
- Sanitize user input to prevent prompt injection
- Rate limit chat endpoints to prevent abuse

### Error Handling
- Graceful degradation when Groq API unavailable
- User-friendly error messages (hide technical details)
- Retry logic for transient Groq API errors
- Logging for debugging tool execution failures

### Performance
- Index database queries on user_id and conversation_id
- Cache tool schemas (don't regenerate on each request)
- Consider connection pooling for database
- Monitor Groq API latency and rate limits

---

## Technology Stack Summary

**Backend**:
- Python 3.13+
- FastAPI (web framework)
- SQLModel (ORM)
- OpenAI Python SDK (Groq client)
- Pydantic (validation)
- pytest (testing)

**Frontend**:
- Next.js 16+ (App Router)
- React 18+
- TypeScript
- Vercel AI SDK (`useChat` hook)
- Tailwind CSS (styling)

**Infrastructure**:
- Neon Serverless PostgreSQL (database)
- Groq (LLM provider)
- Vercel (frontend deployment)

---

## Open Questions

None - all technical decisions finalized based on requirements and constitution mandates.
