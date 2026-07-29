from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Favorite


class FavoriteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_id: UUID, tool_slug: str) -> Favorite:
        fav = Favorite(user_id=user_id, tool_slug=tool_slug)
        self.session.add(fav)
        await self.session.commit()
        await self.session.refresh(fav)
        return fav

    async def remove(self, user_id: UUID, tool_slug: str) -> bool:
        stmt = delete(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.tool_slug == tool_slug,
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def list_by_user(self, user_id: UUID) -> list[Favorite]:
        result = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_id)
        )
        return list(result.scalars().all())

    async def is_favorite(self, user_id: UUID, tool_slug: str) -> bool:
        result = await self.session.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.tool_slug == tool_slug,
            )
        )
        return result.scalar_one_or_none() is not None
