"""
Password hashing and verification using bcrypt via passlib.
Implements secure password handling per FR-004 requirements.
"""

from passlib.context import CryptContext

# Bcrypt password context
# Automatically handles salting and secure hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password string

    Returns:
        str: Bcrypt-hashed password string

    Example:
        hashed = hash_password("mysecretpassword")
        # Returns: $2b$12$...
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt-hashed password from database

    Returns:
        bool: True if password matches, False otherwise

    Example:
        is_valid = verify_password("mysecretpassword", user.hashed_password)
    """
    return pwd_context.verify(plain_password, hashed_password)
