"""One failing certificate must not stop the rest of the job."""

from app.models import CertificateStatus, GenerationJob, JobStatus
from app.services import generation_service
from app.services.generation_service import GenerationService
from tests.helpers import get_job, make_payload, person, submit_job


def _four_people():
    return make_payload(
        [person("Alice One"), person("Bob Broken"), person("Carol Three"), person("Dave Four")]
    )


def test_failure_of_one_certificate_does_not_stop_the_others(client, monkeypatch):
    real_generate = generation_service.generate_certificate_pdf

    def flaky_generate(data, output_path):
        if data.recipient_name == "Bob Broken":
            raise RuntimeError("simulated renderer crash with internal details")
        real_generate(data, output_path)

    monkeypatch.setattr(generation_service, "generate_certificate_pdf", flaky_generate)

    job = get_job(client, submit_job(client, _four_people()))

    # Recipient 2 failed, recipients 3 and 4 (after the failure) still succeeded.
    assert [c["status"] for c in job["certificates"]] == [
        "SUCCESS",
        "FAILED",
        "SUCCESS",
        "SUCCESS",
    ]
    assert job["status"] == "COMPLETED_WITH_ERRORS"
    assert (job["successful_count"], job["failed_count"]) == (3, 1)
    assert job["progress_percent"] == 100.0

    failed = job["certificates"][1]
    assert failed["download_url"] is None
    assert failed["error_message"] == "Certificate PDF could not be generated."
    # Internal details must not leak to the client.
    assert "simulated" not in failed["error_message"]
    assert job["certificates"][0]["download_url"] is not None


def test_job_is_failed_when_every_certificate_fails(client, monkeypatch):
    def always_fail(data, output_path):
        raise RuntimeError("boom")

    monkeypatch.setattr(generation_service, "generate_certificate_pdf", always_fail)

    job = get_job(client, submit_job(client))

    assert job["status"] == "FAILED"
    assert (job["successful_count"], job["failed_count"]) == (0, 2)


def test_unexpected_crash_never_leaves_the_job_stuck(client, session_factory, monkeypatch):
    """If something outside a single recipient breaks, the job still ends."""
    original = GenerationService._generate_one
    calls = {"count": 0}

    def crash_on_second_call(self, job, certificate):
        calls["count"] += 1
        if calls["count"] == 2:
            raise RuntimeError("database went away")
        original(self, job, certificate)

    monkeypatch.setattr(GenerationService, "_generate_one", crash_on_second_call)

    job_id = submit_job(client, _four_people())

    with session_factory() as db:
        job = db.get(GenerationJob, job_id)
        statuses = [c.status for c in job.certificates]
        assert job.status == JobStatus.FAILED
        assert job.completed_at is not None
        assert statuses == [
            CertificateStatus.SUCCESS,
            CertificateStatus.FAILED,
            CertificateStatus.FAILED,
            CertificateStatus.FAILED,
        ]
        assert (job.successful_count, job.failed_count) == (1, 3)
