from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.history_repo import HistoryRepository
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    history_id: UUID
    format: str = "markdown"


def get_service(db: AsyncSession = Depends(get_db)) -> ExportService:
    return ExportService(HistoryRepository(db))


@router.post("")
async def export_entry(
    req: ExportRequest,
    user_id: str = Query(...),
    service: ExportService = Depends(get_service),
):
    try:
        content, filename, media_type = await service.export(
            req.history_id, UUID(user_id), req.format
        )
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
