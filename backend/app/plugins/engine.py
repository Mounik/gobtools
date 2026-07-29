import time
import uuid

from app.domain.schemas import RunRequest, RunResponse
from app.plugins.loader import plugin_loader
from app.providers.registry import provider_registry
from app.core.config import settings


class PluginEngine:
    async def execute(self, req: RunRequest) -> RunResponse:
        manifest = plugin_loader.get(req.tool_slug)
        if manifest is None:
            raise ValueError(f"Outil introuvable : {req.tool_slug}")

        system_prompt = plugin_loader.get_prompt(req.tool_slug)

        provider_name = req.provider or manifest.provider or settings.LLM_PROVIDER
        model = req.model or manifest.model or settings.LLM_MODEL
        temperature = req.temperature if req.temperature is not None else manifest.temperature
        max_tokens = req.max_tokens or manifest.max_tokens

        provider_cls = provider_registry.get(provider_name)
        provider = provider_cls(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=settings.LLM_TIMEOUT,
        )

        start = time.monotonic()
        output = await provider.generate(system_prompt, req.input)
        duration = int((time.monotonic() - start) * 1000)

        return RunResponse(
            id=str(uuid.uuid4()),
            output=output,
            provider=provider_name,
            model=model,
            duration_ms=duration,
        )

    async def execute_stream(self, req: RunRequest):
        manifest = plugin_loader.get(req.tool_slug)
        if manifest is None:
            raise ValueError(f"Outil introuvable : {req.tool_slug}")

        system_prompt = plugin_loader.get_prompt(req.tool_slug)

        provider_name = req.provider or manifest.provider or settings.LLM_PROVIDER
        model = req.model or manifest.model or settings.LLM_MODEL
        temperature = req.temperature if req.temperature is not None else manifest.temperature
        max_tokens = req.max_tokens or manifest.max_tokens

        provider_cls = provider_registry.get(provider_name)
        provider = provider_cls(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=settings.LLM_TIMEOUT,
        )

        async for chunk in provider.stream(system_prompt, req.input):
            yield chunk


plugin_engine = PluginEngine()
