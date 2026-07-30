from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.v1 import export, favorites, history, kanban, run, tools, upload
from app.plugins.loader import plugin_loader
from app.providers.anthropic import AnthropicProvider
from app.providers.gemini import GeminiProvider
from app.providers.mistral import MistralProvider
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.openrouter import OpenRouterProvider
from app.providers.registry import provider_registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    provider_registry.register("ollama", OllamaProvider)
    provider_registry.register("openai", OpenAIProvider)
    provider_registry.register("anthropic", AnthropicProvider)
    provider_registry.register("gemini", GeminiProvider)
    provider_registry.register("mistral", MistralProvider)
    provider_registry.register("openrouter", OpenRouterProvider)

    plugin_loader.load_all()
    yield


app = FastAPI(
    title="GobTools API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tools.router, prefix="/api/v1")
app.include_router(run.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(favorites.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(kanban.router, prefix="/api/v1")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
