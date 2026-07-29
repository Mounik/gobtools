from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.schemas import FavoriteItem
from app.repositories.favorite_repo import FavoriteRepository
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])


class AddFavoriteRequest(BaseModel):
    tool_slug: str


def get_service(db: AsyncSession = Depends(get_db)) -> FavoriteService:
    return FavoriteService(FavoriteRepository(db))


@router.get("")
async def list_favorites(
    user_id: str = Query(...),
    service: FavoriteService = Depends(get_service),
) -> list[FavoriteItem]:
    return await service.list_favorites(UUID(user_id))


@router.post("")
async def add_favorite(
    req: AddFavoriteRequest,
    user_id: str = Query(...),
    service: FavoriteService = Depends(get_service),
) -> dict:
    await service.add_favorite(UUID(user_id), req.tool_slug)
    return {"ok": True}


@router.delete("/{tool_slug}")
async def remove_favorite(
    tool_slug: str,
    user_id: str = Query(...),
    service: FavoriteService = Depends(get_service),
) -> dict:
    deleted = await service.remove_favorite(UUID(user_id), tool_slug)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favori introuvable")
    return {"ok": True}
