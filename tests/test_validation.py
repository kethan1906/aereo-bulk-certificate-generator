"""Input validation: request-level (HTTP 422) and recipient-level (FAILED)."""

import pytest

from app.core.config import settings
from app.models import GenerationJob
from app.utils.validators import validate_recipient
from tests.helpers import JOBS_URL, get_job, make_payload, person, submit_job


def _without(key: str) -> dict:
    payload = make_payload()
    del payload[key]
    return payload


INVALID_REQUESTS = {
    "missing event_name": _without("event_name"),
    "blank event_name": make_payload(event_name="   "),
    "missing event_date": _without("event_date"),
    "malformed event_date": make_payload(event_date="not-a-date"),
    "missing issuer_name": _without("issuer_name"),
    "missing recipients": _without("recipients"),
    "empty recipients list": make_payload(recipients=[]),
    "recipient without email": make_payload(recipients=[{"name": "No Email"}]),
    "recipient name wrong type": make_payload(
        recipients=[{"name": 123, "email": "a@example.com"}]
    ),
    "too many recipients": make_payload(
        recipients=[person("Bulk Person")] * (settings.max_recipients_per_job + 1)
    ),
}


@pytest.mark.parametrize("payload", INVALID_REQUESTS.values(), ids=INVALID_REQUESTS.keys())
def test_invalid_request_is_rejected_with_422_and_creates_no_job(
    client, session_factory, payload
):
    response = client.post(JOBS_URL, json=payload)

    assert response.status_code == 422
    with session_factory() as db:
        assert db.query(GenerationJob).count() == 0


def test_invalid_recipients_are_marked_failed_and_valid_ones_still_succeed(client):
    recipients = [
        {"name": "", "email": "empty@example.com"},
        {"name": "Bad Email", "email": "not-an-email"},
        {"name": "శ్రీనివాస్", "email": "telugu@example.com"},
        {"name": "Valid Person", "email": "valid@example.com"},
    ]
    job_id = submit_job(client, make_payload(recipients))

    job = get_job(client, job_id)
    results = job["certificates"]

    assert [r["status"] for r in results] == ["FAILED", "FAILED", "FAILED", "SUCCESS"]
    assert "name must not be empty" in results[0]["error_message"]
    assert "not a valid email" in results[1]["error_message"]
    assert "cannot display" in results[2]["error_message"]
    assert results[3]["error_message"] is None
    assert job["status"] == "COMPLETED_WITH_ERRORS"
    assert (job["successful_count"], job["failed_count"]) == (1, 3)


@pytest.mark.parametrize(
    ("name", "email", "expected"),
    [
        ("John Doe", "john@example.com", None),
        ("José Müller", "jose@example.com", None),
        ("", "john@example.com", "Recipient name must not be empty."),
        ("   ", "john@example.com", "Recipient name must not be empty."),
        ("John", "john-at-example.com", "Recipient email is not a valid email address."),
        ("John", "john@example", "Recipient email is not a valid email address."),
        ("John", "", "Recipient email is not a valid email address."),
        ("A" * 101, "john@example.com", "Recipient name must be at most 100 characters."),
    ],
)
def test_validate_recipient(name, email, expected):
    assert validate_recipient(name, email) == expected
