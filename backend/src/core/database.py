"""
Database connection and session management using SQLModel.
Implements connection pooling per ADR-003 specifications.
"""

from sqlalchemy.pool import QueuePool
from sqlmodel import Session, create_engine

from .config import settings

# Create SQLModel engine with connection pooling
# ADR-003: pool_size=10, max_overflow=20, pool_pre_ping=True
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,              # Max 10 persistent connections
    max_overflow=20,           # Up to 30 total under load
    pool_pre_ping=True,        # Verify connections before use
    pool_recycle=3600,         # Recycle connections after 1 hour
    echo=settings.DEBUG,       # Log SQL queries in debug mode
)


def get_session():
    """
    FastAPI dependency for database sessions.

    Yields:
        Session: SQLModel database session

    Usage:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session
