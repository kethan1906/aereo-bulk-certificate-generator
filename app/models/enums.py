"""Status values stored in the database.

Inheriting from ``str`` makes the values JSON-friendly ("SUCCESS" not 1).
"""

import enum


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"  # accepted, waiting for the background task
    PROCESSING = "PROCESSING"  # background task is generating certificates
    COMPLETED = "COMPLETED"  # every certificate succeeded
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"  # some succeeded, some failed
    FAILED = "FAILED"  # no certificate succeeded (or the job crashed)


class CertificateStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
