"""
Authentication service for user registration and login.
Implements FR-001 through FR-008 requirements.
"""

import re
from typing import Optional

from sqlmodel import Session, select

from src.auth.password import hash_password, verify_password
from src.models.user import User


def validate_email(email: str) -> bool:
    """
    Validate email format per FR-002.

    Args:
        email: Email address to validate

    Returns:
        bool: True if valid email format

    Example:
        validate_email("user@example.com")  # True
        validate_email("invalid")  # False
    """
    # Simple email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """
    Validate password meets minimum requirements per FR-003.

    Requirements:
        - Minimum 8 characters

    Args:
        password: Password to validate

    Returns:
        bool: True if password meets requirements
    """
    return len(password) >= 8


def register_user(session: Session, email: str, password: str) -> User:
    """
    Register a new user with email and password.

    Implements FR-001 (user registration), FR-002 (email validation),
    FR-003 (password requirements), FR-004 (password hashing).

    Args:
        session: Database session
        email: User email address
        password: Plaintext password

    Returns:
        User: Created user object

    Raises:
        ValueError: If email invalid, password too short, or email already exists

    Example:
        user = register_user(session, "user@example.com", "securepass123")
    """
    # Validate email format (FR-002)
    if not validate_email(email):
        raise ValueError("Invalid email format")

    # Validate password length (FR-003)
    if not validate_password(password):
        raise ValueError("Password must be at least 8 characters")

    # Check if email already exists
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Hash password (FR-004)
    hashed_password = hash_password(password)

    # Create user record (FR-001)
    user = User(
        email=email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user by email and password.

    Implements FR-005 (user login), FR-008 (password verification).

    Args:
        session: Database session
        email: User email address
        password: Plaintext password

    Returns:
        User: Authenticated user object if credentials valid, None otherwise

    Example:
        user = authenticate_user(session, "user@example.com", "securepass123")
        if user:
            # Login successful
            token = create_access_token({"sub": str(user.id)})
    """
    # Find user by email (FR-005)
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return None

    # Verify password hash (FR-008)
    if not verify_password(password, user.hashed_password):
        return None

    return user
