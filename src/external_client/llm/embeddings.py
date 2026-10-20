from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from langchain_openai import OpenAIEmbeddings

from external_client.config import EmbeddingConfig


def create_embeddings(config: EmbeddingConfig, **overrides: Any) -> OpenAIEmbeddings:
    kwargs: dict[str, Any] = {
        "model": config.model,
        "api_key": config.api_key,
        "base_url": config.base_url,
        "timeout": config.timeout_seconds,
        "max_retries": config.max_retries,
        **config.extra,
        **overrides,
    }
    if config.dimensions is not None:
        kwargs["dimensions"] = config.dimensions
    return OpenAIEmbeddings(**kwargs)


def embed_texts(embeddings: Any, texts: Sequence[str]) -> list[list[float]]:
    return embeddings.embed_documents(list(texts))


def embed_query(embeddings: Any, text: str) -> list[float]:
    return embeddings.embed_query(text)
