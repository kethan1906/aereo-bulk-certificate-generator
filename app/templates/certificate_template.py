"""The single predefined certificate template (landscape A4).

The design lives here, separate from the code that saves files, so changing
how the certificate looks never touches the processing logic.
"""

from dataclasses import dataclass
from datetime import date

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

PAGE_SIZE = landscape(A4)
NAVY = HexColor("#1F3A5F")
GOLD = HexColor("#B8903A")
GREY = HexColor("#555555")


@dataclass(frozen=True)
class CertificateData:
    """Everything the template needs to fill in one certificate."""

    certificate_id: str
    recipient_name: str
    event_name: str
    event_date: date
    issuer_name: str


def _fit_font_size(text: str, font: str, max_size: int, max_width: float) -> int:
    """Shrink the font until the text fits inside ``max_width``."""
    size = max_size
    while size > 12 and stringWidth(text, font, size) > max_width:
        size -= 2
    return size


def draw_certificate(pdf: Canvas, data: CertificateData) -> None:
    width, height = PAGE_SIZE
    centre = width / 2
    usable_width = width - 160

    # Double border.
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(4)
    pdf.rect(30, 30, width - 60, height - 60)
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.rect(42, 42, width - 84, height - 84)

    # Title.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 38)
    pdf.drawCentredString(centre, height - 120, "CERTIFICATE OF PARTICIPATION")
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.line(centre - 150, height - 138, centre + 150, height - 138)

    # Recipient.
    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(centre, height - 185, "This is to certify that")

    name_size = _fit_font_size(data.recipient_name, "Helvetica-Bold", 34, usable_width)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", name_size)
    pdf.drawCentredString(centre, height - 235, data.recipient_name)

    # Event.
    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(centre, height - 280, "has successfully participated in")

    event_size = _fit_font_size(data.event_name, "Helvetica-Bold", 26, usable_width)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", event_size)
    pdf.drawCentredString(centre, height - 320, data.event_name)

    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        centre, height - 350, f"held on {data.event_date.strftime('%d %B %Y')}"
    )

    # Issuer.
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1)
    pdf.line(centre - 100, 115, centre + 100, 115)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(centre, 95, data.issuer_name)
    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(centre, 80, "Issued by")

    # Footer: certificate ID so the document can be traced back to the database.
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(centre, 55, f"Certificate ID: {data.certificate_id}")
