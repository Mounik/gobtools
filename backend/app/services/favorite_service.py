from uuid import UUID

from app.domain.schemas import FavoriteItem
from app.plugins.loader import plugin_loader
from app.repositories.favorite_repo import FavoriteRepository


class FavoriteService:
    def __init__(self, repo: FavoriteRepository):
        self.repo = repo

    async def add_favorite(self, user_id: UUID, tool_slug: str) -> None:
        await self.repo.add(user_id, tool_slug)

    async def remove_favorite(self, user_id: UUID, tool_slug: str) -> bool:
        return await self.repo.remove(user_id, tool_slug)

    async def list_favorites(self, user_id: UUID) -> list[FavoriteItem]:
        favs = await self.repo.list_by_user(user_id)
        items: list[FavoriteItem] = []
        for fav in favs:
            manifest = plugin_loader.get(fav.tool_slug)
            if manifest:
                items.append(
                    FavoriteItem(
                        tool_slug=manifest.slug,
                        name=manifest.name,
                        icon=manifest.icon,
                    )
                )
        return items
