# AI Chatbot Testing Guide

**Feature**: 003-ai-chatbot
**Date**: 2026-01-22
**Purpose**: Comprehensive testing plan for all implemented user stories

---

## Pre-Testing Checklist

### 1. Environment Setup

**Backend:**
```bash
cd backend

# Verify environment variables
cat .env | grep -E "GROQ_API_KEY|DATABASE_URL|JWT_SECRET"

# Expected output:
# GROQ_API_KEY=gsk_...
# DATABASE_URL=postgresql://...
# JWT_SECRET=...
```

**Database:**
```bash
# Verify migrations applied
cd backend
alembic current

# Expected: Should show revision 003
```

**Frontend:**
```bash
cd frontend

# Verify environment variables
cat .env.local | grep NEXT_PUBLIC_API_URL

# Expected output:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000

# Expected: Server running on http://localhost:8000
# Check: Visit http://localhost:8000/docs for API docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev

# Expected: Server running on http://localhost:3000
# Check: Visit http://localhost:3000
```

---

## Test Suite 1: User Story 1 - Natural Language Task Management (P1)

### Test 1.1: Basic Task Creation

**Objective**: Verify AI can create tasks from natural language

**Steps:**
1. Navigate to `http://localhost:3000/chat`
2. Login with test credentials
3. Send message: "Add a task to buy groceries tomorrow"

**Expected Result:**
- ✅ User message appears immediately
- ✅ Loading indicator shows "AI is thinking..."
- ✅ Assistant responds with confirmation
- ✅ Task is created in database

**Verification:**
```bash
# Check task was created
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Expected: Task with title "buy groceries" and due_date tomorrow
```

**Success Criteria:**
- [ ] Message sent successfully
- [ ] AI response received within 5 seconds
- [ ] Task appears in task list
- [ ] Due date is correctly set to tomorrow

---

### Test 1.2: List Tasks

**Objective**: Verify AI can retrieve and display tasks

**Steps:**
1. In chat interface, send: "Show me all my tasks"

**Expected Result:**
- ✅ AI lists all user's tasks
- ✅ Includes task titles, status, priority
- ✅ Response is formatted clearly

**Success Criteria:**
- [ ] All tasks displayed
- [ ] Task details are accurate
- [ ] Response is human-readable

---

### Test 1.3: Update Task

**Objective**: Verify AI can modify existing tasks

**Steps:**
1. Send: "Mark the groceries task as completed"

**Expected Result:**
- ✅ AI confirms task updated
- ✅ Task status changes to "completed"

**Verification:**
```bash
# Check task status updated
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Expected: Task status = "completed"
```

**Success Criteria:**
- [ ] Task status updated correctly
- [ ] AI confirms the change
- [ ] Database reflects the update

---

### Test 1.4: Delete Task

**Objective**: Verify AI can delete tasks

**Steps:**
1. Send: "Delete the groceries task"

**Expected Result:**
- ✅ AI confirms deletion
- ✅ Task removed from database

**Success Criteria:**
- [ ] Task deleted successfully
- [ ] Task no longer appears in list

---

### Test 1.5: Complex Query

**Objective**: Verify AI handles multi-parameter requests

**Steps:**
1. Send: "Add a high priority task to finish the report by Friday with notes about including charts"

**Expected Result:**
- ✅ Task created with:
  - Title: "finish the report"
  - Priority: "high"
  - Due date: Next Friday
  - Notes: "including charts"

**Success Criteria:**
- [ ] All parameters captured correctly
- [ ] AI interprets "Friday" as next Friday
- [ ] Priority set to "high"

---

## Test Suite 2: User Story 2 - Conversational Context Awareness (P2)

### Test 2.1: Multi-Turn Conversation

**Objective**: Verify AI maintains context across messages

**Steps:**
1. Send: "Add a task to call the dentist"
2. Wait for response
3. Send: "Set it to high priority"
4. Wait for response
5. Send: "And make the due date tomorrow"

**Expected Result:**
- ✅ AI understands "it" refers to dentist task
- ✅ Task priority updated to "high"
- ✅ Due date set to tomorrow
- ✅ No need to repeat task name

**Success Criteria:**
- [ ] AI correctly resolves pronouns
- [ ] Context maintained across 3 messages
- [ ] Final task has all attributes

---

### Test 2.2: Conversation History Display

**Objective**: Verify message history persists and displays

**Steps:**
1. Send 5 different messages
2. Refresh the page
3. Check if messages are still visible

**Expected Result:**
- ✅ All messages persist after refresh
- ✅ Messages display in chronological order
- ✅ Timestamps are correct

**Success Criteria:**
- [ ] Message history loads on page refresh
- [ ] Order is preserved
- [ ] No messages lost

---

### Test 2.3: Conversation Switching

**Objective**: Verify users can switch between conversations

**Steps:**
1. Create first conversation with 3 messages
2. Click "New Conversation" button
3. Send message in new conversation
4. Click on first conversation in sidebar
5. Verify messages from first conversation appear

**Expected Result:**
- ✅ Sidebar shows both conversations
- ✅ Clicking conversation loads its messages
- ✅ Current conversation highlighted in sidebar
- ✅ Message counts accurate

**Success Criteria:**
- [ ] Sidebar displays all conversations
- [ ] Switching works smoothly
- [ ] No message mixing between conversations
- [ ] Preview text shows first user message

---

### Test 2.4: Conversation Deletion

**Objective**: Verify conversations can be deleted

**Steps:**
1. Create a test conversation
2. Click delete icon on conversation in sidebar
3. Confirm deletion
4. Verify conversation removed

**Expected Result:**
- ✅ Confirmation dialog appears
- ✅ Conversation deleted from sidebar
- ✅ Messages deleted from database

**Success Criteria:**
- [ ] Delete confirmation works
- [ ] Conversation removed from UI
- [ ] Database cascade delete works

---

### Test 2.5: Context Window Management

**Objective**: Verify long conversations are truncated properly

**Steps:**
1. Send 30+ messages in one conversation
2. Check backend logs for truncation
3. Verify AI still responds correctly

**Expected Result:**
- ✅ Logs show context window management
- ✅ Most recent messages retained
- ✅ AI maintains coherent responses

**Success Criteria:**
- [ ] No errors with long conversations
- [ ] Token limit respected (6000 tokens)
- [ ] Recent context preserved

---

## Test Suite 3: User Story 3 - Intelligent Task Suggestions (P3)

### Test 3.1: Overdue Task Suggestion

**Objective**: Verify AI suggests reviewing overdue tasks

**Setup:**
```bash
# Create an overdue task via API
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Old task",
    "due_date": "2026-01-15",
    "status": "pending"
  }'
```

**Steps:**
1. Send: "What should I work on today?"

**Expected Result:**
- ✅ AI mentions overdue task
- ✅ Suggestion formatted with 💡 icon
- ✅ Suggestion box has blue styling

**Success Criteria:**
- [ ] Overdue task detected
- [ ] Suggestion appears in response
- [ ] Visual styling applied

---

### Test 3.2: Missing Due Date Suggestion

**Objective**: Verify AI suggests adding due dates

**Steps:**
1. Send: "Add a task to prepare presentation"
2. Wait for response
3. Check if AI suggests adding a due date

**Expected Result:**
- ✅ Task created without due date
- ✅ AI suggests: "This sounds time-sensitive. Would you like to set a due date?"

**Success Criteria:**
- [ ] Suggestion appears for time-sensitive tasks
- [ ] Suggestion is contextually appropriate

---

### Test 3.3: Vague Description Suggestion

**Objective**: Verify AI suggests adding details

**Steps:**
1. Send: "Add task: work"

**Expected Result:**
- ✅ Task created with brief title
- ✅ AI suggests adding more details

**Success Criteria:**
- [ ] AI detects vague description
- [ ] Suggestion is helpful

---

### Test 3.4: Suggestion Display Styling

**Objective**: Verify suggestions are visually distinct

**Steps:**
1. Trigger any suggestion
2. Inspect the message display

**Expected Result:**
- ✅ Suggestion has blue background
- ✅ 💡 icon appears
- ✅ "SUGGESTION" label visible
- ✅ Border-left styling applied

**Success Criteria:**
- [ ] Visual distinction clear
- [ ] Styling matches design
- [ ] Readable and attractive

---

## Test Suite 4: Error Handling & Edge Cases

### Test 4.1: Empty Message

**Steps:**
1. Try to send empty message

**Expected Result:**
- ✅ Send button disabled or error shown
- ✅ No API call made

---

### Test 4.2: Invalid Conversation ID

**Steps:**
1. Manually set conversation_id to 99999 in API call

**Expected Result:**
- ✅ 403 Forbidden error
- ✅ Error message: "Conversation not found or access denied"

---

### Test 4.3: Groq Rate Limit

**Steps:**
1. Send 35 messages rapidly (exceeds 30/min limit)

**Expected Result:**
- ✅ Error message: "I'm currently experiencing high demand..."
- ✅ User can retry after waiting

---

### Test 4.4: Network Error

**Steps:**
1. Stop backend server
2. Try to send message

**Expected Result:**
- ✅ Error displayed in UI
- ✅ User message removed (optimistic update rollback)

---

### Test 4.5: Invalid JWT Token

**Steps:**
1. Use expired or invalid token

**Expected Result:**
- ✅ 401 Unauthorized error
- ✅ Redirect to login page

---

## Test Suite 5: Performance & Polish

### Test 5.1: Response Time

**Objective**: Verify responses are fast

**Steps:**
1. Send 10 different messages
2. Measure response times

**Expected Result:**
- ✅ 95% of responses < 5 seconds
- ✅ Simple queries < 3 seconds

---

### Test 5.2: Loading States

**Objective**: Verify loading indicators work

**Steps:**
1. Send message
2. Observe UI during processing

**Expected Result:**
- ✅ "AI is thinking..." appears
- ✅ Input disabled during processing
- ✅ Loading indicator disappears when done

---

### Test 5.3: Error Display

**Objective**: Verify errors are user-friendly

**Steps:**
1. Trigger various errors
2. Check error messages

**Expected Result:**
- ✅ No technical jargon
- ✅ Clear actionable messages
- ✅ Red error styling

---

### Test 5.4: Mobile Responsiveness

**Objective**: Verify UI works on mobile

**Steps:**
1. Open chat on mobile device or resize browser
2. Test all features

**Expected Result:**
- ✅ Sidebar collapses or adapts
- ✅ Messages readable
- ✅ Input field accessible

---

## Test Suite 6: Database & Backend

### Test 6.1: Database Indexes

**Objective**: Verify indexes exist for performance

**Steps:**
```bash
psql $DATABASE_URL -c "
SELECT tablename, indexname
FROM pg_indexes
WHERE tablename IN ('conversations', 'messages')
ORDER BY tablename, indexname;
"
```

**Expected Result:**
- ✅ idx_conversations_user_id
- ✅ idx_conversations_updated_at
- ✅ idx_messages_conversation_id
- ✅ idx_messages_created_at

---

### Test 6.2: Cascade Delete

**Objective**: Verify deleting conversation deletes messages

**Steps:**
```bash
# Create conversation and messages via API
# Then delete conversation
# Check messages table
```

**Expected Result:**
- ✅ All messages deleted when conversation deleted

---

### Test 6.3: Logging

**Objective**: Verify comprehensive logging

**Steps:**
1. Send a message
2. Check backend console logs

**Expected Result:**
- ✅ "Processing message for user X"
- ✅ "Calling Groq API with N messages"
- ✅ "Tool execution complete: X/Y successful"
- ✅ "Saved assistant response"

---

## Test Results Summary

### User Story 1 (P1) - Natural Language Task Management
- [ ] Test 1.1: Basic Task Creation
- [ ] Test 1.2: List Tasks
- [ ] Test 1.3: Update Task
- [ ] Test 1.4: Delete Task
- [ ] Test 1.5: Complex Query

### User Story 2 (P2) - Conversational Context Awareness
- [ ] Test 2.1: Multi-Turn Conversation
- [ ] Test 2.2: Conversation History Display
- [ ] Test 2.3: Conversation Switching
- [ ] Test 2.4: Conversation Deletion
- [ ] Test 2.5: Context Window Management

### User Story 3 (P3) - Intelligent Task Suggestions
- [ ] Test 3.1: Overdue Task Suggestion
- [ ] Test 3.2: Missing Due Date Suggestion
- [ ] Test 3.3: Vague Description Suggestion
- [ ] Test 3.4: Suggestion Display Styling

### Error Handling & Edge Cases
- [ ] Test 4.1: Empty Message
- [ ] Test 4.2: Invalid Conversation ID
- [ ] Test 4.3: Groq Rate Limit
- [ ] Test 4.4: Network Error
- [ ] Test 4.5: Invalid JWT Token

### Performance & Polish
- [ ] Test 5.1: Response Time
- [ ] Test 5.2: Loading States
- [ ] Test 5.3: Error Display
- [ ] Test 5.4: Mobile Responsiveness

### Database & Backend
- [ ] Test 6.1: Database Indexes
- [ ] Test 6.2: Cascade Delete
- [ ] Test 6.3: Logging

---

## Known Issues & Limitations

1. **Groq Free Tier**: 30 requests/minute limit
2. **Context Window**: Limited to ~6000 tokens (truncates older messages)
3. **No Streaming**: Responses not streamed (could be added as enhancement)

---

## Next Steps After Testing

1. **If all tests pass**: Ready for deployment
2. **If tests fail**: Document failures and create bug fix tasks
3. **Performance issues**: Profile and optimize
4. **User feedback**: Gather and iterate
