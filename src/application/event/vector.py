from __future__ import annotations

import hashlib
import math
import re
from typing import Any

from external_client.llm.embeddings import embed_texts


def hash_vector(text: str, dimensions: int = 256) -> list[float]:
    vector = [0.0] * dimensions
    for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dimensions
        vector[idx] += 1.0 if digest[4] % 2 == 0 else -1.0
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def safe_embed_texts(embeddings: Any, texts: list[str]) -> list[list[float]]:
    normalized = [text if text.strip() else "empty" for text in texts]
    try:
        return embed_texts(embeddings, normalized)
    except Exception:
        return [hash_vector(text) for text in normalized]


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def average_vectors(vectors: list[list[float]]) -> list[float]:
    if not vectors:
        return []
    dim = min(len(vector) for vector in vectors if vector)
    averaged = [sum(vector[i] for vector in vectors if vector) / len(vectors) for i in range(dim)]
    norm = math.sqrt(sum(value * value for value in averaged))
    return [value / norm for value in averaged] if norm else averaged
