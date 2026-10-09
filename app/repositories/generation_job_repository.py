"""Database access for GenerationJob. No business rules live here.

Repositories never call ``commit()``. The service decides where a
transaction starts and ends.
"""

from sqlalchemy.orm import Session

from app.models.generation_job import GenerationJob


class GenerationJobRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, job: GenerationJob) -> GenerationJob:
        self.db.add(job)
        self.db.flush()  # sends the INSERT so job.id is available
        return job

    def get(self, job_id: str) -> GenerationJob | None:
        return self.db.get(GenerationJob, job_id)
