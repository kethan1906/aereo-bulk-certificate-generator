"""GenerationJob: one bulk request containing many recipients."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import JobStatus
from app.utils.time_utils import utc_now


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_name: Mapped[str] = mapped_column(String(200))
    event_date: Mapped[date] = mapped_column(Date)
    issuer_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, native_enum=False), default=JobStatus.PENDING, index=True
    )
    total_recipients: Mapped[int] = mapped_column(Integer, default=0)
    successful_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # One job -> many certificates. Deleting a job deletes its certificate rows.
    certificates: Mapped[list["Certificate"]] = relationship(  # noqa: F821
        back_populates="job",
        cascade="all, delete-orphan",
        order_by="Certificate.position",
    )

    @property
    def progress_percent(self) -> float:
        """Share of recipients that are finished (successfully or not)."""
        if self.total_recipients == 0:
            return 0.0
        done = self.successful_count + self.failed_count
        return round(done / self.total_recipients * 100, 1)
