from fastapi import APIRouter, HTTPException, Query

from app.domain.schemas import HistoryEntry, PaginatedHistory
from app.services import history_store

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
) -> PaginatedHistory:
    if search:
        items, total = history_store.search_history(search, page, page_size)
    else:
        items, total = history_store.list_history(page, page_size)
    return PaginatedHistory(
        items=[HistoryEntry(**i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.delete("/{entry_id}")
async def delete_history(entry_id: str) -> dict:
    deleted = history_store.delete_entry(entry_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entrée introuvable")
    return {"ok": True}
