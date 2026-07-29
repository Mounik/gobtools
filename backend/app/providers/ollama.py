import httpx

from app.core.config import settings
from app.providers.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = "qwen2.5:1.5b",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: int = 60,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")

    async def generate(
        self, system_prompt: str, user_input: str, **kwargs
    ) -> str:
        payload = {
            "model": kwargs.get("model", self.model),
            "system": system_prompt,
            "prompt": user_input,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate", json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")

    async def stream(self, system_prompt: str, user_input: str, **kwargs):
        payload = {
            "model": kwargs.get("model", self.model),
            "system": system_prompt,
            "prompt": user_input,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST", f"{self.base_url}/api/generate", json=payload
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.strip():
                        import json
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk

    async def healthcheck(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False
