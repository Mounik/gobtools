from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ToolInfo(BaseModel):
    slug: str
    name: str
    description: str = ""
    icon: str = "wand"
    provider: str = "ollama"
    model: str = "qwen3"
    temperature: float = 0.2
    category: str = "general"


class ToolDetail(ToolInfo):
    prompt: str = ""


class RunRequest(BaseModel):
    tool_slug: str
    input: str = Field(..., min_length=1)
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None


class RunResponse(BaseModel):
    id: str
    output: str
    provider: str
    model: str
    duration_ms: int
    tokens_in: int = 0
    tokens_out: int = 0


class HistoryEntry(BaseModel):
    id: str
    tool_slug: str
    input: str
    output: str
    created_at: datetime
    provider: str
    model: str


class PaginatedHistory(BaseModel):
    items: list[HistoryEntry]
    total: int
    page: int = 1
    page_size: int = 20


class FavoriteItem(BaseModel):
    tool_slug: str
    name: str
    icon: str


class ExportRequest(BaseModel):
    history_id: UUID
    format: str = Field(default="markdown", pattern="^(markdown|txt|json|pdf)$")


class SettingsUpdate(BaseModel):
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    timeout: int | None = None
