"""Application entry point. Run with: uvicorn app.main:app --reload"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.db.session import init_db

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()  # create tables on startup
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Submit many recipients in one request and download PDF certificates.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
