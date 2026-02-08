# Quickstart: AI Chatbot Setup

**Feature**: AI Chatbot for Todo Management
**Date**: 2026-01-18
**Prerequisites**: Phase 2 (Multi-user Todo App) must be deployed

## Overview

This guide walks you through setting up the AI chatbot feature locally and deploying to production. The chatbot uses Groq's Llama 3.3 model to provide natural language task management.

---

## Prerequisites

### Required Software

- **Python 3.13+** with UV package manager
- **Node.js 20+** with npm
- **PostgreSQL** (Neon Serverless recommended)
- **Git**

### Required Accounts

- **Groq Account**: Sign up at [https://console.groq.com](https://console.groq.com)
  - Free tier: 30 requests/minute
  - Get API key from console
- **Neon Account**: Database already configured from Phase 2

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend

# Install Python dependencies using UV
uv pip install openai sqlmodel fastapi pydantic python-dotenv alembic

# Or add to pyproject.toml
uv add openai sqlmodel fastapi pydantic python-dotenv alembic
```

### 2. Configure Environment Variables

Create or update `backend/.env`:

```bash
# Existing from Phase 2
DATABASE_URL=postgresql://user:password@host/database
JWT_SECRET=your-jwt-secret-from-phase2

# New for Phase 3
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1

# Optional: Rate limiting
CHAT_RATE_LIMIT=30  # requests per minute per user
```

**⚠️ Security**: Never commit `.env` to version control. Add to `.gitignore`.

### 3. Run Database Migrations

```bash
cd backend

# Create migration for chat tables
alembic revision --autogenerate -m "Add conversations and messages tables"

# Apply migration
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt conversations messages"
```

**Expected Output**:
```
           List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | conversations   | table | user
 public | messages        | table | user
```

### 4. Test Groq Connection

Create `backend/test_groq.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7
)

print(response.choices[0].message.content)
```

Run test:
```bash
python test_groq.py
```

**Expected Output**: A greeting response from Llama 3.3.

### 5. Start Backend Server

```bash
cd backend

# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Verify**: Visit `http://localhost:8000/docs` to see API documentation.

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend

# Install Vercel AI SDK and dependencies
npm install ai @ai-sdk/openai

# Or using yarn
yarn add ai @ai-sdk/openai
```

### 2. Configure Environment Variables

Create or update `frontend/.env.local`:

```bash
# Existing from Phase 2
NEXT_PUBLIC_API_URL=http://localhost:8000

# New for Phase 3 (if using Next.js API routes)
GROQ_API_KEY=gsk_your_groq_api_key_here  # Only if proxying through Next.js
```

### 3. Start Frontend Development Server

```bash
cd frontend

npm run dev
# or
yarn dev
```

**Verify**: Visit `http://localhost:3000/chat` to see chat interface.

---

## Testing the Integration

### 1. Manual Testing Flow

**Step 1**: Create a user account (if not already done in Phase 2)
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**Step 2**: Login and get JWT token
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

Save the returned JWT token.

**Step 3**: Send a chat message
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Add a task to buy groceries tomorrow"}'
```

**Expected Response**:
```json
{
  "message": "I've added 'buy groceries' to your tasks with a due date of tomorrow.",
  "conversation_id": 1,
  "role": "assistant",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "buy groceries",
        "due_date": "2026-01-19"
      },
      "result": {
        "task_id": 1,
        "status": "created"
      }
    }
  ]
}
```

**Step 4**: Verify task was created
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. Automated Testing

Run backend tests:
```bash
cd backend
pytest tests/integration/test_chat_api.py -v
```

Run frontend tests:
```bash
cd frontend
npm test -- components/chat
```

---

## Common Issues & Troubleshooting

### Issue: "Invalid API key" error

**Cause**: Groq API key not set or incorrect

**Solution**:
1. Verify `GROQ_API_KEY` in `.env`
2. Check key is valid at [https://console.groq.com](https://console.groq.com)
3. Restart backend server after updating `.env`

### Issue: "Rate limit exceeded"

**Cause**: Exceeded Groq free tier limit (30 req/min)

**Solution**:
1. Wait 1 minute before retrying
2. Implement request queuing in backend
3. Consider upgrading Groq plan for production

### Issue: "Conversation not found"

**Cause**: Conversation ID doesn't exist or belongs to different user

**Solution**:
1. Verify conversation_id is correct
2. Check JWT token is for the correct user
3. Start new conversation by omitting conversation_id

### Issue: Tool execution fails

**Cause**: Task operation failed (e.g., invalid task_id)

**Solution**:
1. Check backend logs for detailed error
2. Verify task exists and belongs to user
3. Ensure database migrations ran successfully

### Issue: Frontend can't connect to backend

**Cause**: CORS or network configuration

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check backend CORS settings allow frontend origin
3. Ensure both servers are running

---

## Production Deployment

### Backend (Vercel/Railway/Fly.io)

**Environment Variables**:
```bash
DATABASE_URL=postgresql://...  # Neon production URL
JWT_SECRET=...  # Strong secret for production
GROQ_API_KEY=...  # Production Groq key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1
CHAT_RATE_LIMIT=30
```

**Deployment Command**:
```bash
# Example for Vercel
vercel --prod

# Example for Railway
railway up
```

### Frontend (Vercel)

**Environment Variables**:
```bash
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```

**Deployment Command**:
```bash
vercel --prod
```

### Database Migrations

Run migrations on production database:
```bash
# Set production DATABASE_URL
export DATABASE_URL=postgresql://production-url

# Run migrations
alembic upgrade head
```

---

## Performance Optimization

### Backend

1. **Connection Pooling**: Configure SQLAlchemy pool size
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=10,
       max_overflow=20
   )
   ```

2. **Caching**: Cache tool schemas (don't regenerate per request)
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=1)
   def get_tool_schemas():
       return load_tool_schemas()
   ```

3. **Rate Limiting**: Implement per-user rate limiting
   ```python
   from slowapi import Limiter

   limiter = Limiter(key_func=get_user_id)

   @app.post("/api/chat/message")
   @limiter.limit("30/minute")
   async def send_message(...):
       ...
   ```

### Frontend

1. **Message Streaming**: Use streaming for real-time responses
   ```typescript
   const { messages, isLoading } = useChat({
     api: '/api/chat/message',
     streamMode: 'text'  // Enable streaming
   });
   ```

2. **Optimistic Updates**: Show user message immediately
   ```typescript
   const handleSubmit = async (message: string) => {
     // Add message to UI immediately
     setMessages([...messages, { role: 'user', content: message }]);

     // Then send to backend
     await sendMessage(message);
   };
   ```

---

## Monitoring & Logging

### Backend Logging

Add structured logging:
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/api/chat/message")
async def send_message(...):
    logger.info(f"Chat message from user {user_id}", extra={
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message_length": len(message)
    })
```

### Metrics to Track

- **Response Time**: p50, p95, p99 latency for chat endpoint
- **Tool Execution Rate**: How often each tool is called
- **Error Rate**: Failed requests / total requests
- **Groq API Usage**: Requests per minute, token usage
- **Conversation Length**: Average messages per conversation

---

## Next Steps

1. ✅ Backend and frontend running locally
2. ✅ Groq integration tested
3. ✅ Database migrations applied
4. ⏭️ Run `/sp.tasks` to generate implementation tasks
5. ⏭️ Implement P1 user story (Natural Language Task Management)
6. ⏭️ Deploy to production

---

## Additional Resources

- **Groq Documentation**: [https://console.groq.com/docs](https://console.groq.com/docs)
- **OpenAI SDK Docs**: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)
- **Vercel AI SDK**: [https://sdk.vercel.ai/docs](https://sdk.vercel.ai/docs)
- **SQLModel Docs**: [https://sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- **FastAPI Docs**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review backend logs: `tail -f backend/logs/app.log`
3. Check Groq API status: [https://status.groq.com](https://status.groq.com)
4. Consult feature specification: `specs/003-ai-chatbot/spec.md`
