import time
import uuid
from uuid import UUID

from app.core.config import settings
from app.domain.models import History
from app.domain.schemas import RunRequest, RunResponse
from app.plugins.loader import plugin_loader
from app.plugins.models import PluginManifest
from app.providers.registry import provider_registry
from app.repositories.history_repo import HistoryRepository


class ToolService:
    def __init__(self, history_repo: HistoryRepository):
        self.history_repo = history_repo

    def list_tools(self) -> list[PluginManifest]:
        return plugin_loader.list_all()

    def get_tool(self, slug: str) -> PluginManifest | None:
        return plugin_loader.get(slug)

    def get_tool_prompt(self, slug: str) -> str:
        return plugin_loader.get_prompt(slug)

    async def execute(
        self, user_id: UUID | None, req: RunRequest
    ) -> RunResponse:
        manifest = plugin_loader.get(req.tool_slug)
        if manifest is None:
            raise ValueError(f"Outil introuvable : {req.tool_slug}")

        system_prompt = plugin_loader.get_prompt(req.tool_slug)

        provider_name = req.provider or manifest.provider or settings.LLM_PROVIDER
        model = req.model or settings.LLM_MODEL or manifest.model
        temperature = (
            req.temperature
            if req.temperature is not None
            else manifest.temperature
        )
        max_tokens = req.max_tokens or manifest.max_tokens

        provider_cls = provider_registry.get(provider_name)
        provider = provider_cls(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=settings.LLM_TIMEOUT,
        )

        start = time.monotonic()
        try:
            output = await provider.generate(system_prompt, req.input)
        except Exception as e:
            raise ConnectionError(
                f"Impossible de contacter le fournisseur '{provider_name}'. "
                f"Vérifiez que le service est accessible. Détail : {e}"
            ) from e
        duration = int((time.monotonic() - start) * 1000)

        response = RunResponse(
            id=str(uuid.uuid4()),
            output=output,
            provider=provider_name,
            model=model,
            duration_ms=duration,
        )

        if user_id:
            history_entry = History(
                id=uuid.UUID(response.id),
                user_id=user_id,
                tool_slug=req.tool_slug,
                input=req.input,
                output=output,
                provider=provider_name,
                model=model,
                duration_ms=duration,
                temperature=temperature,
            )
            await self.history_repo.create(history_entry)

        return response
