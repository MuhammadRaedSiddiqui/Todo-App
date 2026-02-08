"""
Configuration management using Pydantic BaseSettings.
Loads environment variables with type validation.
"""

from pydantic_settings import BaseSettings
from typing import Optional


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
        GROQ_API_KEY: Groq API key for AI chatbot (Phase 3)
        GROQ_MODEL: Groq model name (default: llama-3.3-70b-versatile)
        GROQ_BASE_URL: Groq API base URL (default: https://api.groq.com/openai/v1)
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

    # Groq AI Configuration (Phase 3)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

    # OpenAI-compatible fields (for compatibility with existing .env)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None
    OPENAI_TEMPERATURE: Optional[float] = None
    OPENAI_MAX_TOKENS: Optional[int] = None

    # MCP Server Configuration
    MCP_SERVER_NAME: Optional[str] = None
    MCP_SERVER_VERSION: Optional[str] = None

    # Chat Rate Limiting
    CHAT_RATE_LIMIT: Optional[int] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

