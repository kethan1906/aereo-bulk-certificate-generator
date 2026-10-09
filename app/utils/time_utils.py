"""Small time helper shared by the models and services."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
