"""Database access for Certificate. No business rules live here."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.certificate import Certificate
from app.models.enums import CertificateStatus


class CertificateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_many(self, certificates: list[Certificate]) -> None:
        self.db.add_all(certificates)
        self.db.flush()

    def get(self, certificate_id: str) -> Certificate | None:
        return self.db.get(Certificate, certificate_id)

    def list_by_status(
        self, job_id: str, status: CertificateStatus
    ) -> list[Certificate]:
        statement = (
            select(Certificate)
            .where(Certificate.job_id == job_id, Certificate.status == status)
            .order_by(Certificate.position)
        )
        return list(self.db.scalars(statement))

    def count_by_status(self, job_id: str) -> dict[CertificateStatus, int]:
        """SELECT status, COUNT(*) ... GROUP BY status for one job."""
        statement = (
            select(Certificate.status, func.count())
            .where(Certificate.job_id == job_id)
            .group_by(Certificate.status)
        )
        return {status: count for status, count in self.db.execute(statement)}
