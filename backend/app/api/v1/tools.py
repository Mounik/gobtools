from fastapi import APIRouter, HTTPException

from app.domain.schemas import ToolDetail, ToolInfo
from app.plugins.loader import plugin_loader

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
async def list_tools() -> list[ToolInfo]:
    manifests = plugin_loader.list_all()
    return [
        ToolInfo(
            slug=m.slug,
            name=m.name,
            description=m.description,
            icon=m.icon,
            provider=m.provider,
            model=m.model,
            temperature=m.temperature,
            category=m.category,
        )
        for m in manifests
    ]


@router.get("/{slug}")
async def get_tool(slug: str) -> ToolDetail:
    manifest = plugin_loader.get(slug)
    if manifest is None:
        raise HTTPException(status_code=404, detail="Outil introuvable")

    prompt = plugin_loader.get_prompt(slug)
    return ToolDetail(
        slug=manifest.slug,
        name=manifest.name,
        description=manifest.description,
        icon=manifest.icon,
        provider=manifest.provider,
        model=manifest.model,
        temperature=manifest.temperature,
        category=manifest.category,
        prompt=prompt,
    )
