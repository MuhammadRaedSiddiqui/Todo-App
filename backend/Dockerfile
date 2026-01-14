# Backend Dockerfile for Todo App
# Python 3.13-slim with UV package manager

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using UV
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run uvicorn (command overridden in docker-compose.yml for hot reload)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
