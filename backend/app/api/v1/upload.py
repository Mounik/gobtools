from fastapi import APIRouter, HTTPException, UploadFile, File

from app.core.config import settings
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["upload"])

MAX_FILE_SIZE = settings.PDF_MAX_SIZE_MB * 1024 * 1024


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers PDF sont acceptés",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Le fichier dépasse la taille maximale de {settings.PDF_MAX_SIZE_MB} Mo",
        )

    try:
        text = extract_text_from_pdf(content)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Impossible d'extraire le texte du PDF : {e}",
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Aucun texte n'a pu être extrait de ce PDF",
        )

    return {
        "filename": file.filename,
        "text": text,
        "length": len(text),
    }
