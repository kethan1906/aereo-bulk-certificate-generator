"""Shared fixtures.

Every test gets its own temporary SQLite database and its own temporary
output folder, so tests never touch real data and never affect each other.
"""

import pytest
from fastapi.testclient import TestClient

import app.models  # noqa: F401  (registers the tables on Base.metadata)
from app.api.deps import get_db, get_session_factory, get_settings
from app.core.config import Settings
from app.db.base import Base
from app.db.session import create_db_engine, create_session_factory
from app.main import app


@pytest.fixture
def test_settings(tmp_path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        generated_dir=tmp_path / "generated",
    )


@pytest.fixture
def session_factory(test_settings):
    engine = create_db_engine(test_settings.database_url)
    Base.metadata.create_all(bind=engine)
    yield create_session_factory(engine)
    engine.dispose()


@pytest.fixture
def client(test_settings, session_factory):
    """A test client whose app uses the temporary database and folder.

    Note: TestClient runs background tasks before ``client.post`` returns, so
    after a POST the job has already been processed.
    """

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session_factory] = lambda: session_factory
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield TestClient(app)
    app.dependency_overrides.clear()
