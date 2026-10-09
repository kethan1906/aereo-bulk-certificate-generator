"""HTTP endpoints for generation jobs."""

from collections.abc import Callable

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_session_factory, get_settings
from app.core.config import Settings
from app.models.enums import CertificateStatus
from app.models.generation_job import GenerationJob
from app.schemas.generation_job import (
    CertificateResult,
    GenerationJobCreate,
    JobCreatedResponse,
    JobStatusResponse,
)
from app.services.generation_service import GenerationService, run_job_in_background

router = APIRouter(prefix="/generation-jobs", tags=["Generation jobs"])


@router.post(
    "",
    response_model=JobCreatedResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a bulk certificate generation job",
)
def create_generation_job(
    payload: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    session_factory: Callable[[], Session] = Depends(get_session_factory),
    settings: Settings = Depends(get_settings),
) -> JobCreatedResponse:
    job = GenerationService(db, settings.generated_dir).create_job(payload)

    # Runs after the response has been sent, so the client is not kept waiting.
    background_tasks.add_task(
        run_job_in_background, job.id, session_factory, settings.generated_dir
    )

    return JobCreatedResponse(
        job_id=job.id,
        status=job.status,
        total_recipients=job.total_recipients,
        status_url=f"/api/v1/generation-jobs/{job.id}",
    )


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Get job status, progress and per-certificate results",
)
def get_generation_job(
    job_id: str,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> JobStatusResponse:
    job = GenerationService(db, settings.generated_dir).get_job(job_id)
    return _to_status_response(job)


def _to_status_response(job: GenerationJob) -> JobStatusResponse:
    results = [
        CertificateResult(
            certificate_id=certificate.id,
            recipient_name=certificate.recipient_name,
            recipient_email=certificate.recipient_email,
            status=certificate.status,
            download_url=(
                f"/api/v1/certificates/{certificate.id}"
                if certificate.status == CertificateStatus.SUCCESS
                else None
            ),
            error_message=certificate.error_message,
        )
        for certificate in job.certificates
    ]
    return JobStatusResponse(
        job_id=job.id,
        event_name=job.event_name,
        event_date=job.event_date,
        issuer_name=job.issuer_name,
        status=job.status,
        total_recipients=job.total_recipients,
        successful_count=job.successful_count,
        failed_count=job.failed_count,
        progress_percent=job.progress_percent,
        created_at=job.created_at,
        completed_at=job.completed_at,
        certificates=results,
    )
