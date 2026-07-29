import httpx
import pytest
import respx

from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.registry import provider_registry


@pytest.mark.asyncio
async def test_ollama_generate():
    provider = OllamaProvider(model="qwen3", temperature=0.2)

    with respx.mock:
        route = respx.post("http://localhost:11434/api/generate").respond(
            json={"response": "TEST OK"},
        )

        result = await provider.generate(
            system_prompt="Be helpful", user_input="Hello"
        )
        assert result == "TEST OK"
        assert route.called


@pytest.mark.asyncio
async def test_openai_generate():
    import app.core.config as cfg
    cfg.settings.OPENAI_API_KEY = "sk-test"

    provider = OpenAIProvider(model="gpt-4o", temperature=0.2)

    with respx.mock:
        route = respx.post("https://api.openai.com/v1/chat/completions").respond(
            json={
                "choices": [
                    {"message": {"content": "Hello from OpenAI"}}
                ]
            },
        )

        result = await provider.generate(
            system_prompt="Be helpful", user_input="Hi"
        )
        assert result == "Hello from OpenAI"
        assert route.called


@pytest.mark.asyncio
async def test_provider_healthcheck_fail():
    provider = OllamaProvider()

    with respx.mock:
        respx.get("http://localhost:11434/api/tags").respond(status_code=503)
        healthy = await provider.healthcheck()
        assert healthy is False


def test_provider_registry():
    provider_cls = provider_registry.get("ollama")
    assert provider_cls is OllamaProvider

    with pytest.raises(ValueError, match="Fournisseur inconnu"):
        provider_registry.get("unknown")


def test_list_providers():
    providers = provider_registry.list_providers()
    assert "ollama" in providers
    assert "openai" in providers
