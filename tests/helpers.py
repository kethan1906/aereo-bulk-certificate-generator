"""Small helpers shared by several test files."""

JOBS_URL = "/api/v1/generation-jobs"
CERTIFICATES_URL = "/api/v1/certificates"


def make_payload(recipients=None, **overrides) -> dict:
    """Build a valid request body. Any field can be overridden."""
    if recipients is None:
        recipients = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Doe", "email": "jane@example.com"},
        ]
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-01",
        "issuer_name": "AEREO",
        "recipients": recipients,
    }
    payload.update(overrides)
    return payload


def person(name: str) -> dict:
    return {"name": name, "email": f"{name.split()[0].lower()}@example.com"}


def submit_job(client, payload=None) -> str:
    """POST a job and return its id."""
    response = client.post(JOBS_URL, json=payload or make_payload())
    assert response.status_code == 202, response.text
    return response.json()["job_id"]


def get_job(client, job_id: str) -> dict:
    response = client.get(f"{JOBS_URL}/{job_id}")
    assert response.status_code == 200, response.text
    return response.json()
