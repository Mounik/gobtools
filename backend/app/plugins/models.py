from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    name: str
    slug: str = ""
    description: str = ""
    icon: str = "wand"
    provider: str = ""
    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096
    category: str = "general"
    prompt_file: str = "prompt.md"
    has_workflow: bool = False
