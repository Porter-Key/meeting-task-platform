from __future__ import annotations

from uuid import uuid4

import pytest
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_qdrant import QdrantVectorStore
from pydantic import BaseModel

from external_client.config import EmbeddingConfig, LLMProviderConfig, get_config
from external_client.llm.chat import create_chat_model, invoke_text
from external_client.llm.embeddings import create_embeddings
from external_client.llm.streaming import stream_text
from external_client.llm.structured import with_structured_output
from external_client.llm.vectorstores import create_qdrant_vector_store, similarity_search

from utils import port_is_open


class DeterministicEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        lower = text.lower()
        return [
            float(lower.count("alpha") + 1),
            float(lower.count("beta") + 1),
            float(len(text) % 7 + 1),
            1.0,
        ]


class StructuredResult(BaseModel):
    ok: bool


class StructuredCapableModel:
    def with_structured_output(self, schema, *, include_raw: bool = False, **kwargs):
        return {"schema": schema, "include_raw": include_raw, "kwargs": kwargs}


def test_create_chat_model_from_openai_compatible_config() -> None:
    model = create_chat_model(
        LLMProviderConfig(
            name="test",
            base_url="https://example.com/v1",
            api_key="test-key",
            models=["test-model"],
            temperature=0,
        ),
        streaming=True,
    )

    assert model.model_name == "test-model"
    assert str(model.openai_api_base).rstrip("/") == "https://example.com/v1"
    assert model.streaming is True


def test_create_embeddings_from_openai_compatible_config() -> None:
    embeddings = create_embeddings(
        EmbeddingConfig(
            provider="test",
            base_url="https://example.com/v1",
            api_key="test-key",
            model="embedding-model",
        )
    )

    assert embeddings.model == "embedding-model"
    assert str(embeddings.openai_api_base).rstrip("/") == "https://example.com/v1"


def test_invoke_and_stream_text_helpers() -> None:
    model = FakeListChatModel(responses=["hello"])

    assert invoke_text(model, "say hello") == "hello"
    assert "".join(stream_text(model, "say hello")) == "hello"


def test_structured_output_helper_delegates_to_model() -> None:
    result = with_structured_output(
        StructuredCapableModel(),
        StructuredResult,
        include_raw=True,
        method="json_schema",
    )

    assert result["schema"] is StructuredResult
    assert result["include_raw"] is True
    assert result["kwargs"] == {"method": "json_schema"}


@pytest.mark.integration
def test_langchain_qdrant_vectorized_retrieval_live() -> None:
    config = get_config().qdrant
    if not port_is_open(config.host, config.port):
        pytest.skip(f"Qdrant is not reachable on {config.host}:{config.port}")

    embeddings = DeterministicEmbeddings()
    collection_name = f"lc_test_{uuid4().hex}"

    store = QdrantVectorStore.from_texts(
        ["alpha alpha", "beta beta"],
        embedding=embeddings,
        collection_name=collection_name,
        url=config.url,
        host=None if config.url else config.host,
        port=None if config.url else config.port,
        grpc_port=config.grpc_port,
        prefer_grpc=config.prefer_grpc,
        https=config.https,
        api_key=config.api_key,
        timeout=int(config.timeout_seconds),
    )

    try:
        existing_store = create_qdrant_vector_store(
            config,
            collection_name=collection_name,
            embeddings=embeddings,
        )
        docs = similarity_search(existing_store, "alpha", k=1)
        assert docs
        assert docs[0].page_content in {"alpha alpha", "beta beta"}
    finally:
        store.client.delete_collection(collection_name=collection_name)
