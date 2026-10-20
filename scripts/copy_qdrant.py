from __future__ import annotations

import argparse
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models


def _diff(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(exclude_none=True)
    return value


def _collection_names(client: QdrantClient) -> list[str]:
    return [collection.name for collection in client.get_collections().collections]


def _copy_collection(source: QdrantClient, target: QdrantClient, name: str, batch_size: int) -> int:
    config = source.get_collection(name).config
    target.recreate_collection(
        collection_name=name,
        vectors_config=config.params.vectors,
        sparse_vectors_config=config.params.sparse_vectors,
        shard_number=config.params.shard_number,
        replication_factor=config.params.replication_factor,
        write_consistency_factor=config.params.write_consistency_factor,
        on_disk_payload=config.params.on_disk_payload,
        hnsw_config=_diff(config.hnsw_config),
        optimizers_config=_diff(config.optimizer_config),
        wal_config=_diff(config.wal_config),
        quantization_config=_diff(config.quantization_config),
        strict_mode_config=_diff(config.strict_mode_config),
        timeout=60,
    )

    copied = 0
    offset: Any = None
    while True:
        points, offset = source.scroll(
            collection_name=name,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        if points:
            target.upsert(
                collection_name=name,
                points=[
                    models.PointStruct(id=point.id, vector=point.vector or {}, payload=point.payload or {})
                    for point in points
                ],
                wait=True,
            )
            copied += len(points)
        if offset is None:
            break
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy all Qdrant collections between local instances.")
    parser.add_argument("--source-url", default="http://127.0.0.1:6333")
    parser.add_argument("--target-url", default="http://127.0.0.1:16333")
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()

    source = QdrantClient(url=args.source_url)
    target = QdrantClient(url=args.target_url)

    total = 0
    for name in _collection_names(source):
        copied = _copy_collection(source, target, name, args.batch_size)
        total += copied
        print(f"copied collection={name} points={copied}")
    print(f"done collections={len(_collection_names(source))} points={total}")


if __name__ == "__main__":
    main()
