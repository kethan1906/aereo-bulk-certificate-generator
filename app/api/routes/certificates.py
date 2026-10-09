"""HTTP endpoint for downloading a generated certificate."""

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_settings
from app.core.config import Settings
from app.services.generation_service import GenerationService

router = APIRouter(prefix="/certificates", tags=["Certificates"])


@router.get(
    "/{certificate_id}",
    response_class=FileResponse,
    summary="Download a generated certificate (PDF)",
    responses={200: {"content": {"application/pdf": {}}}},
)
def download_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> FileResponse:
    certificate, path = GenerationService(
        db, settings.generated_dir
    ).get_certificate_file(certificate_id)
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"certificate-{certificate.id}.pdf",
    )
