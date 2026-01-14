"""
Authentication API endpoints.
Implements user registration and login per contracts/api-spec.yaml.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session

from src.auth.jwt import create_access_token
from src.core.database import get_session
from src.services.auth_service import authenticate_user, register_user

# Request/Response models per contracts/api-spec.yaml

class RegisterRequest(BaseModel):
    """User registration request body."""
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """User login request body."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Authentication response with JWT token and user info."""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


# API Router
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Implements FR-001, FR-002, FR-003, FR-004.

    Endpoint: POST /api/v1/auth/register

    Request body:
        - email: Valid email address (FR-002)
        - password: Minimum 8 characters (FR-003)

    Returns:
        - 201: User created successfully with JWT token
        - 400: Invalid email/password or email already exists

    Example:
        POST /api/v1/auth/register
        {
            "email": "user@example.com",
            "password": "securepass123"
        }

        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer",
            "user_id": 1,
            "email": "user@example.com"
        }
    """
    try:
        # Register user (validates email and password)
        user = register_user(session, request.email, request.password)

        # Generate JWT token with 7-day expiration (FR-006)
        access_token = create_access_token({"sub": str(user.id)})

        return AuthResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Login with email and password.

    Implements FR-005, FR-006, FR-008.

    Endpoint: POST /api/v1/auth/login

    Request body:
        - email: Registered email address
        - password: User password

    Returns:
        - 200: Login successful with JWT token
        - 401: Invalid credentials

    Example:
        POST /api/v1/auth/login
        {
            "email": "user@example.com",
            "password": "securepass123"
        }

        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer",
            "user_id": 1,
            "email": "user@example.com"
        }
    """
    # Authenticate user (FR-005, FR-008)
    user = authenticate_user(session, request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token with 7-day expiration (FR-006)
    access_token = create_access_token({"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user_id=user.id,
        email=user.email
    )
