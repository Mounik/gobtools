from typing import Type

from app.providers.base import LLMProvider


class ProviderRegistry:
    _providers: dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_cls: Type[LLMProvider]) -> None:
        cls._providers[name] = provider_cls

    @classmethod
    def get(cls, name: str) -> Type[LLMProvider]:
        provider = cls._providers.get(name)
        if provider is None:
            raise ValueError(f"Fournisseur inconnu : {name}")
        return provider

    @classmethod
    def list_providers(cls) -> list[str]:
        return list(cls._providers.keys())


provider_registry = ProviderRegistry()
