"""
Configuration management using Pydantic BaseSettings.
Loads environment variables with type validation.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables:
        DATABASE_URL: PostgreSQL connection string (required)
        BETTER_AUTH_SECRET: Shared secret for JWT verification (required)
        JWT_ALGORITHM: Algorithm for JWT signing (default: HS256)
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration in minutes (default: 10080 = 7 days)
        API_V1_PREFIX: API route prefix (default: /api/v1)
        DEBUG: Debug mode flag (default: False)
    """

    # Database
    DATABASE_URL: str

    # Authentication (Better Auth shared secret)
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"

    # Application Settings
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
