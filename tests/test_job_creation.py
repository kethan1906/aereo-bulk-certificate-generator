"""Creating a generation job."""

from app.models import GenerationJob
from tests.helpers import JOBS_URL, make_payload


def test_create_job_returns_202_with_job_id_and_pending_status(client):
    response = client.post(JOBS_URL, json=make_payload())

    assert response.status_code == 202
    body = response.json()
    assert body["job_id"]
    assert body["status"] == "PENDING"  # the response is sent before processing
    assert body["total_recipients"] == 2
    assert body["status_url"] == f"/api/v1/generation-jobs/{body['job_id']}"


def test_create_job_stores_job_and_one_certificate_per_recipient(client, session_factory):
    response = client.post(JOBS_URL, json=make_payload())
    job_id = response.json()["job_id"]

    with session_factory() as db:
        job = db.get(GenerationJob, job_id)
        assert job.event_name == "Python Workshop"
        assert job.issuer_name == "AEREO"
        assert job.total_recipients == 2
        assert [c.recipient_name for c in job.certificates] == ["John Doe", "Jane Doe"]


def test_one_request_can_contain_many_recipients(client):
    recipients = [
        {"name": f"Person {i}", "email": f"person{i}@example.com"} for i in range(50)
    ]
    response = client.post(JOBS_URL, json=make_payload(recipients))

    assert response.status_code == 202
    assert response.json()["total_recipients"] == 50
