"""
Database configuration and session management.

Sets up SQLAlchemy engine, session factory, and base model class.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Prepare connection args for Render compatibility
connect_args = {}
if (
    settings.database_url.startswith("postgresql://")
    and "localhost" not in settings.database_url
):
    # Production/Render: Use SSL
    connect_args = {"sslmode": "require"}

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.environment == "development",  # Log SQL in dev mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all models
class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


def get_db():
    """
    Dependency for FastAPI routes to get a database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
