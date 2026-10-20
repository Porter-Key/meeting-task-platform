from __future__ import annotations

from qdrant_client import QdrantClient

from external_client.config import QdrantConfig


def create_client(config: QdrantConfig) -> QdrantClient:
    kwargs: dict[str, object] = {
        "prefer_grpc": config.prefer_grpc,
        "timeout": config.timeout_seconds,
    }
    if config.url:
        kwargs["url"] = config.url
    else:
        kwargs["host"] = config.host
        kwargs["port"] = config.port
        kwargs["https"] = config.https
        kwargs["grpc_port"] = config.grpc_port
    if config.api_key:
        kwargs["api_key"] = config.api_key
    return QdrantClient(**kwargs)
