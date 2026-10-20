from __future__ import annotations

from qdrant_client import QdrantClient


def healthcheck(client: QdrantClient) -> bool:
    client.get_collections()
    return True
