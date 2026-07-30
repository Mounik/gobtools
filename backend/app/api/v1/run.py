import uuid

from fastapi import APIRouter, HTTPException

from app.domain.schemas import RunRequest, RunResponse
from app.services.history_store import save_run
from app.services.tool_service import ToolService

router = APIRouter(prefix="/run", tags=["run"])


@router.post("")
async def run_tool(req: RunRequest) -> RunResponse:
    if req.tool_slug.strip() == "":
        raise HTTPException(status_code=400, detail="tool_slug requis")

    service = ToolService()

    try:
        response = await service.execute(req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

    save_run(
        id=response.id or str(uuid.uuid4()),
        tool_slug=req.tool_slug,
        input=req.input,
        output=response.output,
        provider=response.provider,
        model=response.model,
        duration_ms=response.duration_ms,
        temperature=req.temperature or 0.0,
    )

    return response
