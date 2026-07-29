import asyncio
from pathlib import Path
from typing import AsyncGenerator

import pytest
import yaml
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.plugins.loader import plugin_loader
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.registry import provider_registry

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def _setup_providers():
    provider_registry._providers.clear()
    provider_registry.register("ollama", OllamaProvider)
    provider_registry.register("openai", OpenAIProvider)
    yield
    provider_registry._providers.clear()


@pytest.fixture(autouse=True)
def _setup_plugins(tmp_path: Path) -> Path:
    plugin_dir = tmp_path / "plugins" / "test-tool"
    plugin_dir.mkdir(parents=True)

    manifest = {
        "name": "Test Tool",
        "description": "A test tool",
        "icon": "sparkles",
        "provider": "ollama",
        "model": "qwen3",
        "temperature": 0.2,
        "category": "test",
    }
    with open(plugin_dir / "manifest.yaml", "w") as f:
        yaml.dump(manifest, f)

    with open(plugin_dir / "prompt.md", "w") as f:
        f.write("You are a test assistant.\nRespond with: TEST OK")

    import app.core.config as cfg
    cfg.settings.PLUGINS_DIR = str(tmp_path / "plugins")

    plugin_loader.reload()
    yield tmp_path / "plugins"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
