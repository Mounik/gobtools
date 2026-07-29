from uuid import UUID

from app.domain.schemas import HistoryEntry, PaginatedHistory
from app.repositories.history_repo import HistoryRepository


class HistoryService:
    def __init__(self, repo: HistoryRepository):
        self.repo = repo

    async def list_history(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> PaginatedHistory:
        items, total = await self.repo.list_by_user(user_id, page, page_size)
        return PaginatedHistory(
            items=[
                HistoryEntry(
                    id=str(h.id),
                    tool_slug=h.tool_slug,
                    input=h.input,
                    output=h.output,
                    created_at=h.created_at,
                    provider=h.provider,
                    model=h.model,
                )
                for h in items
            ],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def search_history(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20
    ) -> PaginatedHistory:
        items, total = await self.repo.search(user_id, query, page, page_size)
        return PaginatedHistory(
            items=[
                HistoryEntry(
                    id=str(h.id),
                    tool_slug=h.tool_slug,
                    input=h.input,
                    output=h.output,
                    created_at=h.created_at,
                    provider=h.provider,
                    model=h.model,
                )
                for h in items
            ],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def delete_entry(self, entry_id: UUID, user_id: UUID) -> bool:
        return await self.repo.delete(entry_id, user_id)
