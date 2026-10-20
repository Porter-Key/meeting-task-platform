from __future__ import annotations

from typing import Any

from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client.http import models
from langchain_core.documents import Document

from external_client.config import QdrantConfig


def create_qdrant_vector_store(
    config: QdrantConfig,
    *,
    collection_name: str,
    embeddings: Any,
    retrieval_mode: RetrievalMode = RetrievalMode.DENSE,
    distance: models.Distance = models.Distance.COSINE,
    validate_collection_config: bool = True,
    **kwargs: Any,
) -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        collection_name=collection_name,
        embedding=embeddings,
        retrieval_mode=retrieval_mode,
        url=config.url,
        host=None if config.url else config.host,
        port=None if config.url else config.port,
        grpc_port=config.grpc_port,
        prefer_grpc=config.prefer_grpc,
        https=config.https,
        api_key=config.api_key,
        timeout=int(config.timeout_seconds),
        distance=distance,
        validate_collection_config=validate_collection_config,
        **kwargs,
    )


def similarity_search(vector_store: Any, query: str, *, k: int = 4, **kwargs: Any) -> list[Document]:
    return vector_store.similarity_search(query, k=k, **kwargs)
