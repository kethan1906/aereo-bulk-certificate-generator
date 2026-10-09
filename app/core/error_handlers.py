"""Translate exceptions into clean JSON error responses.

Clients only ever see a short message. Stack traces and SQL details are
written to the log, never to the response.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(SQLAlchemyError)
    async def handle_database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.exception("Database error while handling %s", request.url.path)
        return JSONResponse(
            status_code=500, content={"detail": "A database error occurred."}
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error while handling %s", request.url.path)
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error."}
        )
