from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.schemas import RunRequest, RunResponse
from app.repositories.history_repo import HistoryRepository
from app.services.tool_service import ToolService

router = APIRouter(prefix="/run", tags=["run"])


@router.post("")
async def run_tool(
    req: RunRequest,
    db: AsyncSession = Depends(get_db),
) -> RunResponse:
    if req.tool_slug.strip() == "":
        raise HTTPException(status_code=400, detail="tool_slug requis")

    history_repo = HistoryRepository(db)
    service = ToolService(history_repo)

    try:
        return await service.execute(user_id=None, req=req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
