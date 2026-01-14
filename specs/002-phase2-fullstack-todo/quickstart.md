# Quickstart: Phase 2 Full-Stack Todo App

**Feature**: 002-phase2-fullstack-todo
**Purpose**: Get the full-stack monorepo running locally in under 5 minutes

## Prerequisites

- **Docker Desktop** (v20+) installed and running
- **Git** (v2.30+)
- **Node.js** (v20+) and npm (for local development without Docker)
- **Python** (v3.13+) and UV (for local development without Docker)

## Quick Start (Docker Compose - Recommended)

###1. Clone and navigate to repository

```bash
git clone <repository-url>
cd todo-app
git checkout 002-phase2-fullstack-todo
```

### 2. Start all services with Docker Compose

```bash
docker compose up --build
```

**What this does**:
- Starts PostgreSQL database on port 5432
- Starts FastAPI backend on port 8000 with hot reload
- Starts Next.js frontend on port 3000 with hot reload
- All services configured with development environment variables

### 3. Verify services are running

Open in your browser:
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health Check**: http://localhost:8000/api/v1/health

### 4. Apply database migrations

```bash
docker compose exec backend alembic upgrade head
```

### 5. Stop services

```bash
docker compose down
```

To remove volumes (deletes database data):
```bash
docker compose down -v
```

---

## Local Development (Without Docker)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Install dependencies with UV**:
```bash
uv sync
```

3. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and configure:
```env
DATABASE_URL=postgresql://todo_user:todo_pass@localhost:5432/todo_dev
BETTER_AUTH_SECRET=dev-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

4. **Start PostgreSQL** (if not using Docker):
```bash
# Option 1: Use Docker for just the database
docker run -d \
  --name todo-postgres \
  -e POSTGRES_DB=todo_dev \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=todo_pass \
  -p 5432:5432 \
  postgres:16-alpine

# Option 2: Use local PostgreSQL installation
# (Configure connection in .env)
```

5. **Run database migrations**:
```bash
alembic upgrade head
```

6. **Start backend development server**:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend now running at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Set up environment variables**:
```bash
cp .env.example .env.local
```

Edit `.env.local` and configure:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
BETTER_AUTH_SECRET=dev-secret-change-in-production
BETTER_AUTH_URL=http://localhost:3000
```

4. **Start frontend development server**:
```bash
npm run dev
```

Frontend now running at http://localhost:3000

---

## Docker Compose Configuration

**File**: `docker-compose.yml` (repository root)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: todo-postgres
    environment:
      POSTGRES_DB: todo_dev
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo_user -d todo_dev"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: todo-backend
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    environment:
      DATABASE_URL: postgresql://todo_user:todo_pass@postgres:5432/todo_dev
      BETTER_AUTH_SECRET: dev-secret-change-in-production
      JWT_ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 10080
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo-frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
      BETTER_AUTH_SECRET: dev-secret-change-in-production
      BETTER_AUTH_URL: http://localhost:3000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## Backend Dockerfile

**File**: `backend/Dockerfile`

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command will be overridden by docker-compose
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Frontend Dockerfile

**File**: `frontend/Dockerfile`

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose Next.js port
EXPOSE 3000

# Command will be overridden by docker-compose
CMD ["npm", "run", "dev"]
```

---

## Common Tasks

### Run database migrations

```bash
# With Docker Compose
docker compose exec backend alembic upgrade head

# Locally
cd backend && alembic upgrade head
```

### Create a new database migration

```bash
# With Docker Compose
docker compose exec backend alembic revision --autogenerate -m "Description"

# Locally
cd backend && alembic revision --autogenerate -m "Description"
```

### View logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Rebuild services after dependency changes

```bash
docker compose up --build
```

### Access PostgreSQL database

```bash
# With Docker Compose
docker compose exec postgres psql -U todo_user -d todo_dev

# Locally
psql -h localhost -U todo_user -d todo_dev
```

### Run backend tests

```bash
# With Docker Compose
docker compose exec backend pytest

# Locally
cd backend && pytest
```

### Run frontend tests

```bash
# With Docker Compose
docker compose exec frontend npm test

# Locally
cd frontend && npm test
```

### Type check TypeScript

```bash
# With Docker Compose
docker compose exec frontend npm run type-check

# Locally
cd frontend && npm run type-check
```

### Lint code

```bash
# Backend (Python)
docker compose exec backend ruff check src tests

# Frontend (TypeScript/React)
docker compose exec frontend npm run lint
```

---

## Troubleshooting

### Port already in use

If ports 3000, 8000, or 5432 are already in use:

```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change ports in docker-compose.yml
```

### Database connection refused

```bash
# Check PostgreSQL is running
docker compose ps

# Restart PostgreSQL
docker compose restart postgres

# Check health
docker compose exec postgres pg_isready -U todo_user
```

### Hot reload not working

```bash
# Rebuild containers
docker compose up --build

# Check volume mounts are correct in docker-compose.yml
```

### Permission errors in Docker

```bash
# On Linux, you may need to fix ownership
sudo chown -R $USER:$USER .
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/db` |
| `BETTER_AUTH_SECRET` | Shared secret for JWT validation | (required) |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | `10080` (7 days) |
| `API_V1_PREFIX` | API route prefix | `/api/v1` |
| `DEBUG` | Enable debug mode | `false` |

### Frontend (.env.local)

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |
| `BETTER_AUTH_SECRET` | Shared secret for JWT generation | (required) |
| `BETTER_AUTH_URL` | Frontend base URL | `http://localhost:3000` |

---

## Next Steps

1. **Implement Authentication**:
   - Backend: JWT verification middleware
   - Frontend: Better Auth configuration

2. **Implement Task CRUD**:
   - Backend: FastAPI endpoints per `contracts/api-spec.yaml`
   - Frontend: Next.js Server Actions for API calls

3. **Add UI Components**:
   - Registration/Login forms
   - Task list with create/edit/delete
   - Completion toggle checkboxes

4. **Write Tests**:
   - Backend: Contract, integration, and unit tests
   - Frontend: Component and E2E tests

5. **Deploy**:
   - Backend: Docker container to cloud platform
   - Frontend: Vercel or similar edge platform
   - Database: Neon Serverless PostgreSQL

See `specs/002-phase2-fullstack-todo/plan.md` for detailed implementation plan.
