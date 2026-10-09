"""Application configuration.

Settings are read from environment variables so nothing is hard-coded,
but every value has a sensible default so the project runs with zero setup.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

# Project root = the folder that contains the "app" package.
BASE_DIR = Path(__file__).resolve().parents[2]


def _default_database_url() -> str:
    return os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'certificates.db'}")


def _default_generated_dir() -> Path:
    return Path(os.getenv("GENERATED_DIR", str(BASE_DIR / "generated")))


@dataclass(frozen=True)
class Settings:
    """Immutable settings object. Tests create their own instance."""

    database_url: str = field(default_factory=_default_database_url)
    generated_dir: Path = field(default_factory=_default_generated_dir)
    # Upper bound for one request. Keeps a single job's size predictable.
    max_recipients_per_job: int = 1000


settings = Settings()
