"""
JWT token creation and verification using python-jose.
Implements Better Auth shared secret strategy per ADR-002.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from src.core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the given data.

    Args:
        data: Dictionary of claims to encode (typically {"sub": user_id})
        expires_delta: Optional custom expiration time (default: 7 days from settings)

    Returns:
        str: Encoded JWT token

    Example:
        token = create_access_token({"sub": str(user.id)})
        # Returns: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    to_encode = data.copy()

    # Set expiration time (default 7 days per FR-006)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode JWT with BETTER_AUTH_SECRET (shared with frontend per ADR-002)
    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        dict: Decoded token payload if valid, None if invalid

    Example:
        payload = verify_token(token)
        if payload:
            user_id = payload.get("sub")
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
