from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):
    model: str
    temperature: float
    max_tokens: int
    timeout: int

    @abstractmethod
    async def generate(self, system_prompt: str, user_input: str, **kwargs) -> str:
        ...

    @abstractmethod
    async def stream(
        self, system_prompt: str, user_input: str, **kwargs
    ) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def healthcheck(self) -> bool:
        ...
