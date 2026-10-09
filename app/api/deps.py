"""FastAPI dependencies (dependency injection).

Tests replace these with ``app.dependency_overrides`` to use a temporary
database and a temporary output folder.
"""

from collections.abc import Callable, Generator

from sqlalchemy.orm import Session

from app.core.config import Settings, settings
from app.db.session import SessionLocal


def get_settings() -> Settings:
    return settings


def get_session_factory() -> Callable[[], Session]:
    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
