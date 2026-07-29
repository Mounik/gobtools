import json

import httpx

from app.core.config import settings
from app.providers.base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: int = 60,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.api_key = settings.ANTHROPIC_API_KEY
        self.base_url = "https://api.anthropic.com/v1"

    async def generate(
        self, system_prompt: str, user_input: str, **kwargs
    ) -> str:
        payload = {
            "model": kwargs.get("model", self.model),
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_input}],
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/messages",
                json=payload,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]

    async def stream(self, system_prompt: str, user_input: str, **kwargs):
        payload = {
            "model": kwargs.get("model", self.model),
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_input}],
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/messages",
                json=payload,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        data = json.loads(line[6:])
                        if data["type"] == "content_block_delta":
                            delta = data["delta"]
                            if delta["type"] == "text_delta":
                                yield delta["text"]

    async def healthcheck(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(
                    f"{self.base_url}/models",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                    },
                )
                return resp.status_code == 200
        except Exception:
            return False
