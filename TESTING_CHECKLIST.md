# Testing Setup Checklist

## Current Status: ⏸️ Ready to Begin

### Prerequisites Checklist

- [ ] **Step 1: Groq API Key**
  - Get key from https://console.groq.com
  - Add to `backend/.env`
  - Verify with: `cat backend/.env | grep GROQ_API_KEY`

- [ ] **Step 2: Database Migrations**
  - Run: `cd backend && alembic upgrade head`
  - Verify: `alembic current` shows revision 003

- [ ] **Step 3: Backend Server**
  - Run: `cd backend && uvicorn src.main:app --reload --port 8000`
  - Verify: Visit http://localhost:8000/docs

- [ ] **Step 4: Frontend Server**
  - Run: `cd frontend && npm run dev`
  - Verify: Visit http://localhost:3000/chat

- [ ] **Step 5: Run Automated Tests**
  - Run: `bash test-chatbot.sh`
  - All tests should pass

- [ ] **Step 6: Manual UI Testing**
  - Test natural language commands
  - Test conversation switching
  - Test suggestions

---

## Quick Commands Reference

```bash
# Check if Groq key is set
cat backend/.env | grep GROQ_API_KEY

# Run migrations
cd backend && alembic upgrade head

# Start backend (Terminal 1)
cd backend && uvicorn src.main:app --reload --port 8000

# Start frontend (Terminal 2)
cd frontend && npm run dev

# Run tests (Terminal 3)
bash test-chatbot.sh
```

---

## What to Do Right Now

**Option A: I have a Groq API key**
→ Add it to `backend/.env` and continue to Step 2

**Option B: I need to get a Groq API key**
→ Visit https://console.groq.com and sign up (takes 2 minutes)

**Option C: I want to skip AI testing for now**
→ You can test the UI and database without Groq, but AI responses won't work

---

## Tell me which option and I'll guide you through it!
