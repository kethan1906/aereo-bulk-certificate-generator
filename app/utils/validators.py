"""Per-recipient validation.

The request schema only checks the *shape* of the request. Each recipient's
content is checked here so that one bad recipient is recorded as FAILED
instead of rejecting the whole request.
"""

import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 254


def _is_printable_by_certificate_font(text: str) -> bool:
    """The built-in PDF font (Helvetica) only supports Western (cp1252) characters."""
    try:
        text.encode("cp1252")
    except UnicodeEncodeError:
        return False
    return True


def validate_recipient(name: str, email: str) -> str | None:
    """Return an error message if the recipient is invalid, else ``None``."""
    if not name or not name.strip():
        return "Recipient name must not be empty."
    if len(name) > MAX_NAME_LENGTH:
        return f"Recipient name must be at most {MAX_NAME_LENGTH} characters."
    if not _is_printable_by_certificate_font(name):
        return "Recipient name contains characters the certificate font cannot display."
    if not email or len(email) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.match(email):
        return "Recipient email is not a valid email address."
    return None
