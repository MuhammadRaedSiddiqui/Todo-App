# Todo App Backend

FastAPI backend for Todo App with Neon Serverless PostgreSQL.

## Architecture

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Python**: 3.13+

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel classes for database entities
│   ├── services/        # Business logic layer
│   ├── api/             # FastAPI endpoints (RESTful)
│   └── auth/            # JWT verification, user authentication
├── tests/
│   ├── unit/            # Unit tests for models and services
│   ├── integration/     # Integration tests for API endpoints
│   └── contract/        # API contract tests
├── pyproject.toml       # Python dependencies (UV managed)
├── .env.example         # Environment variable template
└── README.md            # This file
```

## Setup

1. Install dependencies with UV:
```bash
uv sync
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Set up Neon PostgreSQL database URL in `.env`

4. Run migrations (once implemented):
```bash
# TBD: Alembic migrations
```

5. Run the development server:
```bash
uvicorn src.main:app --reload
```

## Development

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Run tests: `pytest`
- Run linter: `ruff check src tests`
- Format code: `ruff format src tests`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Constitution Compliance

This backend follows the Todo App Constitution v2.0.0:
- ✅ Principle II: Neon PostgreSQL with SQLModel ORM
- ✅ Principle VI: RESTful API standard (GET, POST, PUT, PATCH, DELETE)
- ✅ Principle VII: Multi-user authentication with JWT, user-scoped data
