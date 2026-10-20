from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yaml"


def _section(data: dict[str, Any], *path: str) -> dict[str, Any]:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return {}
        current = current.get(key, {})
    return current if isinstance(current, dict) else {}


@dataclass(slots=True)
class QdrantConfig:
    host: str = "127.0.0.1"
    port: int = 16333
    grpc_port: int = 16334
    url: str | None = None
    api_key: str | None = None
    prefer_grpc: bool = False
    https: bool = False
    timeout_seconds: float = 10.0
    extra: dict[str, Any] = field(default_factory=dict)

    def endpoint(self) -> str:
        if self.url:
            return self.url
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.host}:{self.port}"


@dataclass(slots=True)
class LLMProviderConfig:
    name: str
    base_url: str
    api_key: str
    models: list[str] = field(default_factory=list)
    default_model: str | None = None
    temperature: float | None = None
    timeout_seconds: float = 60.0
    max_retries: int = 2
    extra: dict[str, Any] = field(default_factory=dict)

    def model_name(self, model: str | None = None) -> str:
        if model:
            return model
        if self.default_model:
            return self.default_model
        if self.models:
            return self.models[0]
        raise ValueError(f"No model configured for LLM provider: {self.name}")


@dataclass(slots=True)
class EmbeddingConfig:
    provider: str = "openrouter"
    base_url: str = ""
    model: str = ""
    api_key: str = ""
    dimensions: int | None = None
    timeout_seconds: float = 60.0
    max_retries: int = 2
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LangChainConfig:
    default_llm_provider: str = "opus5"
    default_embedding_provider: str = "openrouter"
    stream_usage: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FirefliesConfig:
    api_key: str = ""
    graphql_url: str = "https://api.fireflies.ai/graphql"
    timeout_seconds: float = 30.0


@dataclass(slots=True)
class MondayConfig:
    api_token: str = ""
    graphql_url: str = "https://api.monday.com/v2"
    api_version: str = "2026-01"
    timeout_seconds: float = 30.0


@dataclass(slots=True)
class RedisConfig:
    lock_url: str = "redis://127.0.0.1:16380/3"
    query_cache_url: str = "redis://127.0.0.1:16380/2"


@dataclass(slots=True)
class ExternalConfig:
    raw: dict[str, Any]
    qdrant: QdrantConfig
    llm: dict[str, LLMProviderConfig]
    embedding: EmbeddingConfig
    langchain: LangChainConfig
    fireflies: FirefliesConfig
    monday: MondayConfig
    redis: RedisConfig

    def llm_provider(self, name: str | None = None) -> LLMProviderConfig:
        provider_name = name or self.langchain.default_llm_provider
        return self.llm[provider_name]


def load_config(path: str | Path | None = None) -> ExternalConfig:
    config_path = Path(path) if path else _DEFAULT_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return ExternalConfig(
        raw=data,
        qdrant=_parse_qdrant(data),
        llm=_parse_llm(data),
        embedding=_parse_embedding(data),
        langchain=_parse_langchain(data),
        fireflies=_parse_fireflies(data),
        monday=_parse_monday(data),
        redis=_parse_redis(data),
    )


@lru_cache(maxsize=1)
def get_config() -> ExternalConfig:
    return load_config()


def _parse_qdrant(data: dict[str, Any]) -> QdrantConfig:
    section = _section(data, "infra", "qdrant")
    return QdrantConfig(host=section.get("host", "127.0.0.1"), port=int(section.get("port", 16333)), grpc_port=int(section.get("grpc_port", 16334)), url=section.get("url"), api_key=section.get("api_key"), prefer_grpc=bool(section.get("prefer_grpc", False)), https=bool(section.get("https", False)), timeout_seconds=float(section.get("timeout_seconds", 10.0)))


def _parse_llm(data: dict[str, Any]) -> dict[str, LLMProviderConfig]:
    return {name: LLMProviderConfig(name=name, base_url=value.get("base_url", ""), api_key=value.get("api_key", ""), models=list(value.get("models", [])), default_model=value.get("default_model"), temperature=value.get("temperature"), timeout_seconds=float(value.get("timeout_seconds", 60.0)), max_retries=int(value.get("max_retries", 2)), extra={key: item for key, item in value.items() if key not in {"base_url", "api_key", "models", "default_model", "temperature", "timeout_seconds", "max_retries"}}) for name, value in _section(data, "llm").items() if isinstance(value, dict)}


def _parse_embedding(data: dict[str, Any]) -> EmbeddingConfig:
    section = _section(data, "embedding")
    return EmbeddingConfig(provider=section.get("provider", "openrouter"), base_url=section.get("base_url", ""), model=section.get("model", ""), api_key=section.get("api_key", ""), dimensions=section.get("dimensions"), timeout_seconds=float(section.get("timeout_seconds", 60.0)), max_retries=int(section.get("max_retries", 2)), extra={key: value for key, value in section.items() if key not in {"provider", "base_url", "model", "api_key", "dimensions", "timeout_seconds", "max_retries"}})


def _parse_langchain(data: dict[str, Any]) -> LangChainConfig:
    section = _section(data, "infra", "langchain")
    return LangChainConfig(default_llm_provider=section.get("default_llm_provider", "opus5"), default_embedding_provider=section.get("default_embedding_provider", "openrouter"), stream_usage=bool(section.get("stream_usage", False)), extra={key: value for key, value in section.items() if key not in {"default_llm_provider", "default_embedding_provider", "stream_usage"}})


def _parse_fireflies(data: dict[str, Any]) -> FirefliesConfig:
    section = _section(data, "fireflies")
    return FirefliesConfig(api_key=section.get("api_key", ""), graphql_url=section.get("graphql_url", "https://api.fireflies.ai/graphql"), timeout_seconds=float(section.get("timeout_seconds", 30.0)))


def _parse_monday(data: dict[str, Any]) -> MondayConfig:
    section = _section(data, "monday")
    return MondayConfig(api_token=section.get("api_token", ""), graphql_url=section.get("graphql_url", "https://api.monday.com/v2"), api_version=section.get("api_version", "2026-01"), timeout_seconds=float(section.get("timeout_seconds", 30.0)))


def _parse_redis(data: dict[str, Any]) -> RedisConfig:
    section = _section(data, "infra", "redis")
    lock_url = section.get("lock_url", "redis://127.0.0.1:16380/3")
    return RedisConfig(lock_url=lock_url, query_cache_url=section.get("query_cache_url", "redis://127.0.0.1:16380/2"))
