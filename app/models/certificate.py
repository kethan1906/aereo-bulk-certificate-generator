"""Certificate: the result for ONE recipient inside a job."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CertificateStatus
from app.models.generation_job import GenerationJob
from app.utils.time_utils import utc_now


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    job_id: Mapped[str] = mapped_column(
        ForeignKey("generation_jobs.id"), index=True
    )
    # Position of the recipient in the original request (keeps the order stable).
    position: Mapped[int] = mapped_column(Integer)
    recipient_name: Mapped[str] = mapped_column(String(255))
    recipient_email: Mapped[str] = mapped_column(String(255))
    status: Mapped[CertificateStatus] = mapped_column(
        Enum(CertificateStatus, native_enum=False),
        default=CertificateStatus.PENDING,
        index=True,
    )
    # Path of the PDF *relative to* the generated directory. NULL until success.
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    job: Mapped[GenerationJob] = relationship(back_populates="certificates")
