from __future__ import annotations

from uuid import uuid4

import pytest
from qdrant_client.http import models

from external_client.config import get_config
from external_client.qdrant.client import create_client
from external_client.qdrant.collections import ensure_collection
from external_client.qdrant.health import healthcheck

from utils import port_is_open


@pytest.mark.integration
def test_qdrant_live_client_healthcheck_and_collection_helper() -> None:
    config = get_config().qdrant
    if not port_is_open(config.host, config.port):
        pytest.skip(f"Qdrant is not reachable on {config.host}:{config.port}")

    client = create_client(config)
    collection_name = f"infra_test_{uuid4().hex}"

    assert healthcheck(client) is True
    try:
        ensure_collection(
            client,
            name=collection_name,
            vector_size=4,
            distance=models.Distance.COSINE,
        )
        assert client.collection_exists(collection_name=collection_name) is True

        ensure_collection(client, name=collection_name, vector_size=4)
        assert client.collection_exists(collection_name=collection_name) is True
    finally:
        if client.collection_exists(collection_name=collection_name):
            client.delete_collection(collection_name=collection_name)
