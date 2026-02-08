# Quick Start: Testing the AI Chatbot

Follow these steps in order to test the AI Chatbot implementation.

---

## Step 1: Configure Groq API Key ⚙️

### Get Your API Key
1. Visit https://console.groq.com
2. Sign up/login
3. Go to "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_`)

### Add to Environment
Edit `backend/.env` and add:

```bash
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1
```

**Verify:**
```bash
cd backend
cat .env | grep GROQ_API_KEY
# Should show: GROQ_API_KEY=gsk_...
```

---

## Step 2: Run Database Migrations 🗄️

The chatbot needs `conversations` and `messages` tables.

```bash
cd backend

# Check current migration status
alembic current

# If not at revision 003, run migrations
alembic upgrade head

# Verify tables created
# (Replace with your actual DATABASE_URL)
psql $DATABASE_URL -c "\dt conversations messages"
```

**Expected output:**
```
           List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | conversations   | table | ...
 public | messages        | table | ...
```

---

## Step 3: Start Backend Server 🚀

**Terminal 1:**
```bash
cd backend

# Install dependencies if needed
uv sync

# Start server
uvicorn src.main:app --reload --port 8000
```

**Verify:**
- Open http://localhost:8000/docs
- You should see API documentation
- Check for `/api/chat/message` endpoint

**Keep this terminal running!**

---

## Step 4: Start Frontend Server 🎨

**Terminal 2:**
```bash
cd frontend

# Install dependencies if needed
npm install

# Start development server
npm run dev
```

**Verify:**
- Open http://localhost:3000
- You should see the app homepage
- Navigate to http://localhost:3000/chat

**Keep this terminal running!**

---

## Step 5: Run Automated Tests 🧪

**Terminal 3:**
```bash
cd /path/to/todo-app

# Run quick test script
bash test-chatbot.sh
```

**What it tests:**
- ✅ Backend health check
- ✅ User authentication
- ✅ Chat message sending
- ✅ Task creation via AI
- ✅ Multi-turn conversation
- ✅ Conversation history
- ✅ Conversation deletion

**Expected output:**
```
🧪 AI Chatbot Quick Test Script
================================

📋 Pre-flight Checks
-------------------
Checking backend server... ✓ Running
Checking frontend server... ✓ Running
Checking GROQ_API_KEY... ✓ Set

🔐 Authentication
----------------
✓ Authenticated

💬 Test 1: Basic Chat Message
-----------------------------
✓ Chat message sent
Conversation ID: 1
AI Response: I've added "test the chatbot" to your tasks...

📝 Test 2: Verify Task Created
------------------------------
✓ Task created
Total tasks: 1

🔄 Test 3: Multi-Turn Conversation
----------------------------------
✓ Multi-turn conversation works

📚 Test 4: Conversation History
-------------------------------
✓ Conversation history persisted
Messages in conversation: 4

🗑️  Test 5: Conversation Deletion
--------------------------------
✓ Conversation deleted

🎉 Quick tests complete!
```

---

## Step 6: Manual UI Testing 🖱️

### Test User Story 1: Natural Language Task Management

1. **Open chat interface:** http://localhost:3000/chat
2. **Login** with your credentials
3. **Send messages:**
   - "Add a task to buy groceries tomorrow"
   - "Show me all my tasks"
   - "Mark the groceries task as completed"
   - "Delete the groceries task"

**Expected:** AI understands and executes all commands

---

### Test User Story 2: Conversational Context

1. **Send:** "Add a task to call the dentist"
2. **Send:** "Set it to high priority" (uses pronoun "it")
3. **Send:** "And make the due date tomorrow"
4. **Click:** "New Conversation" button
5. **Send:** A new message in the new conversation
6. **Click:** First conversation in sidebar
7. **Verify:** Original messages appear

**Expected:** Context maintained, conversation switching works

---

### Test User Story 3: Intelligent Suggestions

1. **Create overdue task via API or manually set past due date**
2. **Send:** "What should I work on today?"
3. **Look for:** 💡 **Suggestion:** box with blue styling
4. **Send:** "Add task: work" (vague description)
5. **Look for:** Suggestion to add more details

**Expected:** AI proactively suggests improvements

---

## Troubleshooting 🔧

### "Invalid API key" error
- Check GROQ_API_KEY in backend/.env
- Verify key is valid at https://console.groq.com
- Restart backend server after updating .env

### "Rate limit exceeded"
- Groq free tier: 30 requests/minute
- Wait 1 minute before retrying
- Consider upgrading Groq plan

### "Conversation not found"
- Verify JWT token is valid
- Check conversation belongs to logged-in user
- Start new conversation by clicking "New Conversation"

### Backend won't start
- Check DATABASE_URL is correct
- Verify all dependencies installed: `uv sync`
- Check port 8000 is not in use

### Frontend won't start
- Check NEXT_PUBLIC_API_URL in frontend/.env.local
- Verify dependencies installed: `npm install`
- Check port 3000 is not in use

### No AI response
- Check backend logs for errors
- Verify GROQ_API_KEY is set correctly
- Test Groq connection: `python backend/test_groq.py`

---

## Full Test Suite 📋

For comprehensive testing, see:
- **specs/003-ai-chatbot/TESTING.md** - Complete test suite with 30+ test cases

---

## Success Criteria ✅

Your implementation is working if:

- [x] Backend starts without errors
- [x] Frontend loads chat interface
- [x] Can send messages and receive AI responses
- [x] AI creates/updates/deletes tasks correctly
- [x] Conversation history persists
- [x] Can switch between conversations
- [x] Suggestions appear for overdue tasks
- [x] All automated tests pass

---

## Next Steps 🚀

Once testing is complete:

1. **Fix any bugs** found during testing
2. **Deploy to staging** environment
3. **Conduct user acceptance testing**
4. **Deploy to production**
5. **Monitor logs** and performance

---

## Need Help?

- Review implementation: `specs/003-ai-chatbot/`
- Check logs: Backend terminal output
- API docs: http://localhost:8000/docs
- Groq status: https://status.groq.com
