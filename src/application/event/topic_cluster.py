from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.cluster import HDBSCAN

from .vector import average_vectors, cosine, safe_embed_texts


def chunk_text(chunk: dict[str, Any]) -> str:
    return str(chunk.get("text") or "")


LOW_INFORMATION_UTTERANCES = {
    "ok",
    "okay",
    "yes",
    "yeah",
    "yep",
    "no",
    "hello",
    "hi",
    "all right",
    "alright",
    "nice",
    "good",
    "thanks",
    "thank you",
}


LOW_VALUE_TOPIC_PHRASES = {
    "general agreement",
    "general appreciation",
    "appreciation on stage",
    "closing appreciation",
    "closing remark",
    "closing remarks",
    "brief closing",
    "thanks",
    "thank you",
    "greeting",
    "small talk",
}


MIN_EVENT_TOPIC_CONFIDENCE = 0.55
MAX_TOPIC_CORE_CHUNKS = 15
MAX_TOPIC_CLUSTER_CHUNKS = 30


def normalized_chunk_text(chunk: dict[str, Any]) -> str:
    text = chunk_text(chunk).strip().lower()
    for marker in ("raw chunk:", "source sentence indexes:"):
        if marker in text:
            text = text.split(marker, 1)[-1]
    return " ".join(text.replace(".", " ").replace(",", " ").split())


def is_event_candidate_chunk(chunk: dict[str, Any]) -> bool:
    text = normalized_chunk_text(chunk)
    if not text:
        return False
    tokens = text.split()
    if len(tokens) <= 2 and text in LOW_INFORMATION_UTTERANCES:
        return False
    if len(tokens) <= 4 and all(token in LOW_INFORMATION_UTTERANCES for token in tokens):
        return False
    return len(tokens) >= 4


def _normalized_text(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def is_event_worthy_topic(topic: dict[str, Any], *, min_confidence: float = MIN_EVENT_TOPIC_CONFIDENCE) -> bool:
    confidence = topic.get("confidence")
    if confidence is not None:
        try:
            if float(confidence) < min_confidence:
                return False
        except (TypeError, ValueError):
            pass

    text = _normalized_text(" ".join([str(topic.get("title") or ""), str(topic.get("summary") or "")]))
    if not text:
        return False
    if any(phrase in text for phrase in LOW_VALUE_TOPIC_PHRASES):
        return False
    return True


def filter_event_worthy_topics(topics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [topic for topic in topics if is_event_worthy_topic(topic)]


def _hdbscan_labels(matrix: np.ndarray, *, min_cluster_size: int, min_samples: int | None) -> np.ndarray:
    if len(matrix) < min_cluster_size:
        return np.zeros(len(matrix), dtype=int)
    return HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
        allow_single_cluster=True,
    ).fit_predict(matrix)


def _batched_indexes(indexes: list[int], *, batch_size: int) -> list[list[int]]:
    ordered = sorted(indexes)
    return [ordered[start:start + batch_size] for start in range(0, len(ordered), batch_size)]


def _chunk_time_distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    left_start = float(left.get("start_time") or 0.0)
    left_end = float(left.get("end_time") or left_start)
    right_start = float(right.get("start_time") or 0.0)
    right_end = float(right.get("end_time") or right_start)
    if left_end >= right_start and right_end >= left_start:
        return 0.0
    return min(abs(left_start - right_end), abs(right_start - left_end))


def _recall_temporal_noise_indexes(
    *,
    batch: list[int],
    noise: list[int],
    candidate_chunks: list[dict[str, Any]],
    original_indexes: list[int],
    max_total_chunks: int,
) -> list[int]:
    remaining = max_total_chunks - len(batch)
    if remaining <= 0 or not noise:
        return []
    batch_originals = [original_indexes[idx] for idx in batch]
    min_original = min(batch_originals)
    max_original = max(batch_originals)
    scored: list[tuple[int, float, int]] = []
    for idx in noise:
        original = original_indexes[idx]
        chunk_distance = 0 if min_original <= original <= max_original else min(abs(original - min_original), abs(original - max_original))
        time_distance = min(_chunk_time_distance(candidate_chunks[idx], candidate_chunks[batch_idx]) for batch_idx in batch)
        if chunk_distance > 6 and time_distance > 300.0:
            continue
        fact_bonus = 0 if any(char.isdigit() for char in chunk_text(candidate_chunks[idx])) else 1
        scored.append((idx, time_distance, fact_bonus * 1000 + chunk_distance))
    return [idx for idx, _, _ in sorted(scored, key=lambda item: (item[1], item[2], original_indexes[item[0]]))[:remaining]]


def semantic_chunk_clusters(embeddings: Any, chunks: list[dict[str, Any]], *, min_cluster_size: int = 2, min_samples: int | None = 1, max_cluster_chunks: int = MAX_TOPIC_CLUSTER_CHUNKS, max_clusters: int | None = None) -> list[dict[str, Any]]:
    if not chunks:
        return []
    indexed_chunks = [(idx, chunk) for idx, chunk in enumerate(chunks) if is_event_candidate_chunk(chunk)]
    if not indexed_chunks:
        return []
    original_indexes = [idx for idx, _ in indexed_chunks]
    candidate_chunks = [chunk for _, chunk in indexed_chunks]
    vectors = safe_embed_texts(embeddings, [chunk_text(chunk) for chunk in candidate_chunks])
    matrix = np.asarray(vectors, dtype=np.float32)
    matrix = matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)
    labels = np.array([0]) if len(candidate_chunks) == 1 else _hdbscan_labels(matrix, min_cluster_size=min_cluster_size, min_samples=min_samples)
    groups: dict[int, list[int]] = {}
    for idx, label in enumerate(labels.tolist()):
        if int(label) < 0:
            continue
        groups.setdefault(int(label), []).append(idx)
    clusters = []
    hdbscan_groups = list(groups.values())
    noise: list[int] = []
    for idx, label in enumerate(labels.tolist()):
        if int(label) < 0:
            noise.append(idx)
            continue
    used_noise: set[int] = set()
    for group in hdbscan_groups:
        centroid = average_vectors([vectors[idx] for idx in group])
        representatives = sorted(group, key=lambda idx: cosine(vectors[idx], centroid), reverse=True)[:5]
        for batch in _batched_indexes(group, batch_size=min(MAX_TOPIC_CORE_CHUNKS, max_cluster_chunks)):
            retrieved = _recall_temporal_noise_indexes(
                batch=batch,
                noise=[idx for idx in noise if idx not in used_noise],
                candidate_chunks=candidate_chunks,
                original_indexes=original_indexes,
                max_total_chunks=max_cluster_chunks,
            )
            used_noise.update(retrieved)
            combined_batch = sorted(set(batch + retrieved), key=lambda idx: original_indexes[idx])
            batch_original_indexes = [original_indexes[idx] for idx in batch]
            combined_original_indexes = [original_indexes[idx] for idx in combined_batch]
            batch_representatives = [original_indexes[idx] for idx in representatives if idx in batch]
            clusters.append({
                "cluster_id": f"sc_{len(clusters)+1}",
                "chunk_indexes": combined_original_indexes,
                "core_chunk_indexes": batch_original_indexes,
                "retrieved_chunk_indexes": [original_indexes[idx] for idx in retrieved],
                "noise_chunk_indexes": [original_indexes[idx] for idx in retrieved if int(labels[idx]) < 0],
                "representative_indexes": batch_representatives or batch_original_indexes,
                "centroid": average_vectors([vectors[idx] for idx in combined_batch]),
                "size": len(combined_batch),
            })
    sorted_clusters = sorted(clusters, key=lambda item: item["size"], reverse=True)
    return sorted_clusters[:max_clusters] if max_clusters is not None else sorted_clusters


def topic_text(topic: dict[str, Any]) -> str:
    return "\n".join([topic.get("title", ""), topic.get("summary", ""), " ".join(topic.get("keywords") or []), " ".join(topic.get("entities") or [])]).strip()


def cluster_topics(embeddings: Any, topics: list[dict[str, Any]], *, min_cluster_size: int = 2, min_samples: int | None = 1) -> list[dict[str, Any]]:
    if not topics:
        return []
    vectors = safe_embed_texts(embeddings, [topic_text(topic) for topic in topics])
    matrix = np.asarray(vectors, dtype=np.float32)
    matrix = matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)
    labels = np.array([0]) if len(topics) == 1 else _hdbscan_labels(matrix, min_cluster_size=min_cluster_size, min_samples=min_samples)
    groups_by_label: dict[int, list[int]] = {}
    for idx, label in enumerate(labels.tolist()):
        if int(label) < 0:
            continue
        else:
            groups_by_label.setdefault(int(label), []).append(idx)
    groups = list(groups_by_label.values())
    return [{"topic_indexes": group, "vector": average_vectors([vectors[idx] for idx in group])} for group in groups]
