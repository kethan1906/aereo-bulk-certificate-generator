"""Pydantic schemas: what the API accepts and returns."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import settings
from app.models.enums import CertificateStatus, JobStatus


class RecipientIn(BaseModel):
    """One recipient in the request.

    Only the *types* are checked here. Whether the name is non-empty and the
    email is valid is checked per recipient in the service, so a single bad
    recipient does not reject the whole bulk request.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    email: str


class GenerationJobCreate(BaseModel):
    """Body of POST /api/v1/generation-jobs."""

    model_config = ConfigDict(str_strip_whitespace=True)

    event_name: str = Field(min_length=1, max_length=200, examples=["Python Workshop"])
    event_date: date = Field(examples=["2026-10-01"])
    issuer_name: str = Field(min_length=1, max_length=200, examples=["AEREO"])
    recipients: list[RecipientIn] = Field(
        min_length=1, max_length=settings.max_recipients_per_job
    )


class JobCreatedResponse(BaseModel):
    job_id: str
    status: JobStatus
    total_recipients: int
    status_url: str


class CertificateResult(BaseModel):
    certificate_id: str
    recipient_name: str
    recipient_email: str
    status: CertificateStatus
    download_url: str | None = None
    error_message: str | None = None


class JobStatusResponse(BaseModel):
    job_id: str
    event_name: str
    event_date: date
    issuer_name: str
    status: JobStatus
    total_recipients: int
    successful_count: int
    failed_count: int
    progress_percent: float
    created_at: datetime
    completed_at: datetime | None = None
    certificates: list[CertificateResult]
