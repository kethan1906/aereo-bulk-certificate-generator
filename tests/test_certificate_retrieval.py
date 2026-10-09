"""Retrieving generated certificates."""

from tests.helpers import CERTIFICATES_URL, get_job, make_payload, submit_job


def test_generated_certificate_can_be_downloaded_as_pdf(client):
    job = get_job(client, submit_job(client))
    certificate = job["certificates"][0]

    response = client.get(certificate["download_url"])

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
    assert certificate["certificate_id"] in response.headers["content-disposition"]


def test_unknown_certificate_returns_404(client):
    response = client.get(f"{CERTIFICATES_URL}/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"detail": "Certificate not found."}


def test_failed_certificate_has_no_file_to_download(client):
    payload = make_payload(
        [
            {"name": "Valid Person", "email": "valid@example.com"},
            {"name": "Bad Email", "email": "nope"},
        ]
    )
    job = get_job(client, submit_job(client, payload))
    failed = job["certificates"][1]

    response = client.get(f"{CERTIFICATES_URL}/{failed['certificate_id']}")

    assert failed["status"] == "FAILED"
    assert response.status_code == 404
    assert response.json() == {"detail": "Certificate file is not available."}


def test_missing_file_on_disk_returns_404_not_500(client, test_settings):
    job_id = submit_job(client)
    certificate_id = get_job(client, job_id)["certificates"][0]["certificate_id"]
    (test_settings.generated_dir / job_id / f"{certificate_id}.pdf").unlink()

    response = client.get(f"{CERTIFICATES_URL}/{certificate_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Certificate file is not available."}
