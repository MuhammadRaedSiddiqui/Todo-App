"""
FastAPI dependencies for authentication and authorization.
Implements JWT token validation per ADR-002 authentication flow.
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from src.auth.jwt import verify_token
from src.core.database import get_session
from src.models.user import User

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    FastAPI dependency that validates JWT token and returns authenticated User.

    Authentication flow (per ADR-002):
    1. Extract Bearer token from Authorization header
    2. Verify JWT signature using BETTER_AUTH_SECRET
    3. Extract user_id from token payload
    4. Query database for User
    5. Return User object or raise 401

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException: 401 if token invalid or user not found

    Usage:
        @app.get("/tasks")
        def get_tasks(current_user: User = Depends(get_current_user)):
            # current_user is guaranteed to be authenticated
            return {"user_id": current_user.id}
    """
    # Verify JWT token
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from token payload
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Query database for user
    statement = select(User).where(User.id == int(user_id))
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
