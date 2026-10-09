"""Database engine and session setup."""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base


def create_db_engine(database_url: str) -> Engine:
    """Create an engine. Also used by the tests with a temporary database."""
    connect_args = {}
    if database_url.startswith("sqlite"):
        # FastAPI runs sync code in worker threads, so SQLite must allow
        # a connection to be used outside the thread that created it.
        connect_args["check_same_thread"] = False

    engine = create_engine(database_url, connect_args=connect_args)

    if database_url.startswith("sqlite"):
        # SQLite ignores foreign keys unless this pragma is switched on.
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    # autoflush=False: we flush explicitly so it is obvious when SQL runs.
    # expire_on_commit=False: objects stay readable after commit.
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


engine = create_db_engine(settings.database_url)
SessionLocal = create_session_factory(engine)


def init_db() -> None:
    """Create all tables (simple alternative to migrations for this project)."""
    import app.models  # noqa: F401  (registers the models on Base.metadata)

    Base.metadata.create_all(bind=engine)
