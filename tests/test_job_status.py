"""Job status and progress."""

from app.schemas.generation_job import GenerationJobCreate
from app.services.generation_service import GenerationService
from tests.helpers import JOBS_URL, get_job, make_payload, person, submit_job


def test_completed_job_reports_counts_and_full_progress(client):
    job_id = submit_job(client)

    job = get_job(client, job_id)

    assert job["job_id"] == job_id
    assert job["status"] == "COMPLETED"
    assert job["total_recipients"] == 2
    assert job["successful_count"] == 2
    assert job["failed_count"] == 0
    assert job["progress_percent"] == 100.0
    assert job["completed_at"] is not None
    assert job["event_name"] == "Python Workshop"


def test_progress_moves_from_pending_to_completed(client, session_factory, test_settings):
    """Create the job WITHOUT processing it, so we can look at the middle state."""
    recipients = [person("Alice One"), person("Bob Two"), person("Carol Three")]
    recipients.append({"name": "Bad Email", "email": "nope"})
    payload = GenerationJobCreate(**make_payload(recipients))

    with session_factory() as db:
        service = GenerationService(db, test_settings.generated_dir)
        job_id = service.create_job(payload).id

    before = get_job(client, job_id)
    assert before["status"] == "PENDING"
    assert before["failed_count"] == 1  # the invalid recipient is known immediately
    assert before["successful_count"] == 0
    assert before["progress_percent"] == 25.0
    assert before["completed_at"] is None

    with session_factory() as db:
        GenerationService(db, test_settings.generated_dir).process_job(job_id)

    after = get_job(client, job_id)
    assert after["status"] == "COMPLETED_WITH_ERRORS"
    assert (after["successful_count"], after["failed_count"]) == (3, 1)
    assert after["progress_percent"] == 100.0
    assert after["completed_at"] is not None


def test_status_lists_every_recipient_in_request_order(client):
    names = ["Zed Last", "Amy First", "Mia Middle"]
    job_id = submit_job(client, make_payload([person(n) for n in names]))

    job = get_job(client, job_id)

    assert [c["recipient_name"] for c in job["certificates"]] == names


def test_unknown_job_returns_404(client):
    response = client.get(f"{JOBS_URL}/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"detail": "Generation job not found."}
