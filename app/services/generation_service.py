"""Business logic for bulk certificate generation.

Flow:
1. ``create_job``  - validate every recipient, store the job and one
   certificate row per recipient (invalid ones are stored as FAILED).
2. ``process_job`` - generate a PDF for every PENDING certificate. Each
   recipient is handled in its own try/except, so one failure never stops
   the others.
3. ``get_job`` / ``get_certificate_file`` - read results back.
"""

import logging
from collections.abc import Callable
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.exceptions import (
    CertificateFileMissingError,
    CertificateNotFoundError,
    JobNotFoundError,
)
from app.models.certificate import Certificate
from app.models.enums import CertificateStatus, JobStatus
from app.models.generation_job import GenerationJob
from app.repositories.certificate_repository import CertificateRepository
from app.repositories.generation_job_repository import GenerationJobRepository
from app.schemas.generation_job import GenerationJobCreate
from app.services.certificate_pdf_service import generate_certificate_pdf
from app.templates.certificate_template import CertificateData
from app.utils.time_utils import utc_now
from app.utils.validators import validate_recipient

logger = logging.getLogger(__name__)

PDF_FAILURE_MESSAGE = "Certificate PDF could not be generated."


class GenerationService:
    def __init__(self, db: Session, generated_dir: Path) -> None:
        self.db = db
        self.generated_dir = generated_dir
        self.jobs = GenerationJobRepository(db)
        self.certificates = CertificateRepository(db)

    # ------------------------------------------------------------------ create
    def create_job(self, payload: GenerationJobCreate) -> GenerationJob:
        job = GenerationJob(
            event_name=payload.event_name,
            event_date=payload.event_date,
            issuer_name=payload.issuer_name,
            status=JobStatus.PENDING,
            total_recipients=len(payload.recipients),
        )
        self.jobs.add(job)

        certificates: list[Certificate] = []
        for position, recipient in enumerate(payload.recipients):
            error = validate_recipient(recipient.name, recipient.email)
            certificates.append(
                Certificate(
                    job_id=job.id,
                    position=position,
                    recipient_name=recipient.name,
                    recipient_email=recipient.email,
                    status=CertificateStatus.FAILED if error else CertificateStatus.PENDING,
                    error_message=error,
                )
            )
        self.certificates.add_many(certificates)

        job.failed_count = sum(1 for c in certificates if c.error_message)
        self.db.commit()  # one transaction: the job and all its recipients
        return job

    # ----------------------------------------------------------------- process
    def process_job(self, job_id: str) -> None:
        job = self.jobs.get(job_id)
        if job is None:
            logger.error("process_job: job %s does not exist", job_id)
            return

        job.status = JobStatus.PROCESSING
        self.db.commit()

        try:
            for certificate in self.certificates.list_by_status(
                job_id, CertificateStatus.PENDING
            ):
                self._generate_one(job, certificate)
            self._finish_job(job)
        except Exception:
            # Something outside a single recipient broke (e.g. the database).
            logger.exception("Job %s crashed", job_id)
            self._abort_job(job_id)

    def _generate_one(self, job: GenerationJob, certificate: Certificate) -> None:
        relative_path = Path(job.id) / f"{certificate.id}.pdf"
        data = CertificateData(
            certificate_id=certificate.id,
            recipient_name=certificate.recipient_name,
            event_name=job.event_name,
            event_date=job.event_date,
            issuer_name=job.issuer_name,
        )
        try:
            generate_certificate_pdf(data, self.generated_dir / relative_path)
        except Exception:
            # Only THIS recipient fails. The loop in process_job carries on.
            logger.exception("Certificate %s failed", certificate.id)
            certificate.status = CertificateStatus.FAILED
            certificate.error_message = PDF_FAILURE_MESSAGE
        else:
            certificate.status = CertificateStatus.SUCCESS
            certificate.file_path = relative_path.as_posix()

        self._refresh_counts(job)
        self.db.commit()  # commit per recipient so progress is visible live

    def _refresh_counts(self, job: GenerationJob) -> None:
        self.db.flush()
        counts = self.certificates.count_by_status(job.id)
        job.successful_count = counts.get(CertificateStatus.SUCCESS, 0)
        job.failed_count = counts.get(CertificateStatus.FAILED, 0)

    def _finish_job(self, job: GenerationJob) -> None:
        self._refresh_counts(job)
        if job.failed_count == 0:
            job.status = JobStatus.COMPLETED
        elif job.successful_count == 0:
            job.status = JobStatus.FAILED
        else:
            job.status = JobStatus.COMPLETED_WITH_ERRORS
        job.completed_at = utc_now()
        self.db.commit()

    def _abort_job(self, job_id: str) -> None:
        """Last resort: mark unfinished work as failed so the job never hangs."""
        try:
            self.db.rollback()
            job = self.jobs.get(job_id)
            for certificate in self.certificates.list_by_status(
                job_id, CertificateStatus.PENDING
            ):
                certificate.status = CertificateStatus.FAILED
                certificate.error_message = "Job stopped unexpectedly."
            self._refresh_counts(job)
            job.status = JobStatus.FAILED
            job.completed_at = utc_now()
            self.db.commit()
        except Exception:
            logger.exception("Could not mark job %s as failed", job_id)

    # -------------------------------------------------------------------- read
    def get_job(self, job_id: str) -> GenerationJob:
        job = self.jobs.get(job_id)
        if job is None:
            raise JobNotFoundError()
        return job

    def get_certificate_file(self, certificate_id: str) -> tuple[Certificate, Path]:
        certificate = self.certificates.get(certificate_id)
        if certificate is None:
            raise CertificateNotFoundError()
        if certificate.status != CertificateStatus.SUCCESS or not certificate.file_path:
            raise CertificateFileMissingError()
        path = self.generated_dir / certificate.file_path
        if not path.is_file():
            raise CertificateFileMissingError()
        return certificate, path


def run_job_in_background(
    job_id: str, session_factory: Callable[[], Session], generated_dir: Path
) -> None:
    """Entry point for FastAPI's BackgroundTasks.

    The request's database session is closed once the response is sent, so
    the background task must open its OWN session.
    """
    with session_factory() as db:
        GenerationService(db, generated_dir).process_job(job_id)
