"""FastAPI application entry point."""

import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.auth import router as auth_router
from src.api.chat import router as chat_router
from src.api.conversations import router as conversations_router
from src.api.tasks import router as tasks_router
from src.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Todo API",
    description="Multi-user Todo App with Better Auth JWT authentication",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware for frontend communication
# Allow both local development and production frontend
allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://frontend-xi-steel-95.vercel.app",  # Production frontend
]

# Add additional origins from environment variable if set
import os
if cors_origins := os.getenv("CORS_ORIGINS"):
    allowed_origins.extend(cors_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware (T078)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timestamp, method, path, and status code."""
    start_time = time.time()

    # Log incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Log response
    logger.info(
        f"Completed: {request.method} {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.3f}s"
    )

    return response


# Global exception handler (T077)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return 500 with proper error format."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please try again later.",
            "type": "internal_error"
        }
    )


# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed error messages."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


# HTTP exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
def root():
    """
    Root health check endpoint.

    Returns:
        dict: API status and version
    """
    return {
        "status": "ok",
        "message": "Todo API v2.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: Health status
    """
    return {"status": "healthy"}


# Mount API routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(tasks_router, prefix=settings.API_V1_PREFIX)
app.include_router(chat_router, prefix=settings.API_V1_PREFIX)
app.include_router(conversations_router, prefix=settings.API_V1_PREFIX)
