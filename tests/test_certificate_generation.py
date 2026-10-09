"""Certificate generation: the PDF service and the end-to-end result."""

from datetime import date

from app.services.certificate_pdf_service import generate_certificate_pdf
from app.templates.certificate_template import CertificateData
from tests.helpers import get_job, make_payload, submit_job


def test_pdf_service_writes_a_valid_pdf_file(tmp_path):
    data = CertificateData(
        certificate_id="cert-1",
        recipient_name="John Doe",
        event_name="Python Workshop",
        event_date=date(2026, 10, 1),
        issuer_name="AEREO",
    )
    output = tmp_path / "nested" / "cert-1.pdf"

    generate_certificate_pdf(data, output)

    content = output.read_bytes()
    assert content.startswith(b"%PDF")
    assert b"%%EOF" in content[-32:]


def test_pdf_service_handles_very_long_names_and_event_titles(tmp_path):
    data = CertificateData("cert-2", "A" * 100, "Event " * 40, date(2026, 10, 1), "AEREO")
    output = tmp_path / "long.pdf"

    generate_certificate_pdf(data, output)

    assert output.read_bytes().startswith(b"%PDF")


def test_every_valid_recipient_gets_a_pdf_on_disk(client, test_settings):
    job_id = submit_job(client)  # two valid recipients

    job = get_job(client, job_id)

    assert [c["status"] for c in job["certificates"]] == ["SUCCESS", "SUCCESS"]
    for certificate in job["certificates"]:
        pdf_path = test_settings.generated_dir / job_id / f"{certificate['certificate_id']}.pdf"
        assert pdf_path.is_file()
        assert pdf_path.read_bytes().startswith(b"%PDF")


def test_each_certificate_has_its_own_file(client, test_settings):
    job_id = submit_job(client, make_payload())
    job = get_job(client, job_id)

    ids = {c["certificate_id"] for c in job["certificates"]}
    files = {p.stem for p in (test_settings.generated_dir / job_id).glob("*.pdf")}

    assert len(ids) == 2
    assert files == ids
