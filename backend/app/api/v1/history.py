from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.schemas import PaginatedHistory
from app.repositories.history_repo import HistoryRepository
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["history"])


def get_service(db: AsyncSession = Depends(get_db)) -> HistoryService:
    return HistoryService(HistoryRepository(db))


@router.get("")
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    user_id: str = Query(...),
    service: HistoryService = Depends(get_service),
) -> PaginatedHistory:
    uid = UUID(user_id)
    if search:
        return await service.search_history(uid, search, page, page_size)
    return await service.list_history(uid, page, page_size)


@router.delete("/{entry_id}")
async def delete_history(
    entry_id: UUID,
    user_id: str = Query(...),
    service: HistoryService = Depends(get_service),
) -> dict:
    deleted = await service.delete_entry(entry_id, UUID(user_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Entrée introuvable")
    return {"ok": True}
