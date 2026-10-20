from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http import models


def ensure_collection(
    client: QdrantClient,
    *,
    name: str,
    vector_size: int,
    distance: models.Distance = models.Distance.COSINE,
    recreate: bool = False,
) -> None:
    exists = client.collection_exists(collection_name=name)
    if exists and not recreate:
        return
    if exists and recreate:
        client.delete_collection(collection_name=name)
    client.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(size=vector_size, distance=distance),
    )
