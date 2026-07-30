from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from app.services import history_store
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    history_id: str
    format: str = "markdown"


@router.post("")
async def export_entry(req: ExportRequest):
    items, _ = history_store.list_history(page=1, page_size=1000)
    entry = next((h for h in items if h["id"] == req.history_id), None)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entrée introuvable")

    service = ExportService()
    try:
        content, filename, media_type = service.export(entry, req.format)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
