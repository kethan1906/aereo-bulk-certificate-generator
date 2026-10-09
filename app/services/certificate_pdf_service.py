"""Turns a CertificateData object into a PDF file on disk."""

from pathlib import Path

from reportlab.pdfgen.canvas import Canvas

from app.templates.certificate_template import (
    PAGE_SIZE,
    CertificateData,
    draw_certificate,
)


def generate_certificate_pdf(data: CertificateData, output_path: Path) -> None:
    """Render one certificate to ``output_path``.

    Any error is allowed to propagate: the caller (the generation service)
    decides that one failed certificate must not stop the rest of the job.
    A half-written file is deleted so it can never be served by mistake.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        pdf = Canvas(str(output_path), pagesize=PAGE_SIZE)
        pdf.setTitle(f"Certificate - {data.recipient_name}")
        pdf.setAuthor(data.issuer_name)
        draw_certificate(pdf, data)
        pdf.showPage()
        pdf.save()
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
