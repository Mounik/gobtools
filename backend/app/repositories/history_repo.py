from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import History


class HistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entry: History) -> History:
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def list_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[History], int]:
        offset = (page - 1) * page_size

        count_q = select(History).where(History.user_id == user_id)
        total_q = select(History).where(History.user_id == user_id).order_by(
            History.created_at.desc()
        )

        total_result = await self.session.execute(
            select(History.id).where(History.user_id == user_id)
        )
        total = len(total_result.scalars().all())

        result = await self.session.execute(
            total_q.offset(offset).limit(page_size)
        )
        items = list(result.scalars().all())

        return items, total

    async def delete(self, entry_id: UUID, user_id: UUID) -> bool:
        stmt = delete(History).where(
            History.id == entry_id, History.user_id == user_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def search(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20
    ) -> tuple[list[History], int]:
        stmt = (
            select(History)
            .where(
                History.user_id == user_id,
                History.input.ilike(f"%{query}%"),
            )
            .order_by(History.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        count_stmt = select(History).where(
            History.user_id == user_id,
            History.input.ilike(f"%{query}%"),
        )
        count_result = await self.session.execute(count_stmt)
        total = len(count_result.scalars().all())

        return items, total
