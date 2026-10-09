"""Custom exceptions raised by the service layer.

The service layer knows nothing about HTTP. It raises these exceptions and
the handlers in ``error_handlers.py`` translate them into HTTP responses.
"""


class AppError(Exception):
    """Base class for expected, client-facing errors."""

    status_code = 500
    message = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class JobNotFoundError(AppError):
    status_code = 404
    message = "Generation job not found."


class CertificateNotFoundError(AppError):
    status_code = 404
    message = "Certificate not found."


class CertificateFileMissingError(AppError):
    status_code = 404
    message = "Certificate file is not available."
