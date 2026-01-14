# Phase 1: In-Memory Console Todo App Requirements

## 1. Project Overview
We are building **Phase 1** of the "Evolution of Todo" project. This is a simple, command-line interface (CLI) application for managing tasks. 
**Crucial Constraint:** This application must store data **in-memory** (using Python lists or dictionaries). Do not use a database or file persistence for this phase.

## 2. Technology Stack
- **Language:** Python 3.13+
- **Package Manager:** UV
- **Interface:** CLI (Console)
- **Framework:** Standard Python Libraries (no external web frameworks like FastAPI yet)

## 3. Functional Requirements (Basic Level)
The application must support the following 5 core features:
1. **Add Task:** Users can create a new task with a `title` (required) and `description` (optional).
2. **View Task List:** Users can see all tasks with their IDs, Titles, and current Status (Pending/Completed).
3. **Update Task:** Users can modify the title or description of an existing task using its ID.
4. **Mark as Complete:** Users can toggle a task's status from "Pending" to "Completed".
5. **Delete Task:** Users can permanently remove a task using its ID.

## 4. Data Model (In-Memory)
The Task object should minimally contain:
- `id`: Integer (Unique identifier, auto-incrementing)
- `title`: String
- `description`: String
- `status`: String or Boolean (default: "Pending" or False)
- `created_at`: Timestamp

## 5. Non-Functional Requirements
- **Error Handling:** The app should not crash if the user enters invalid IDs.
- **Usability:** The CLI should provide a clear menu loop (e.g., "Press 1 to Add, 2 to View...") until the user chooses to exit.
- **Code Quality:** Follow PEP 8 standards. Code must be modular (separate `main.py` from logic/models).