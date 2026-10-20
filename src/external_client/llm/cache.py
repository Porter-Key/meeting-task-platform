from __future__ import annotations

import hashlib
import logging
import pickle
import tempfile
import threading
from pathlib import Path
from typing import Any

from langchain_core.caches import BaseCache
from langchain_core.globals import set_llm_cache


class StableFileCache(BaseCache):
    """Small durable LangChain cache keyed by stable prompt/model hashes."""

    def __init__(self, path: str | Path = ".cache/langchain_llm") -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def _cache_path(self, prompt: str, llm_string: str) -> Path:
        normalized_prompt = prompt.replace("\r\n", "\n")
        key_material = f"{normalized_prompt}\n---llm---\n{llm_string}"
        digest = hashlib.sha256(key_material.encode("utf-8")).hexdigest()
        return self.path / f"{digest}.pickle"

    def lookup(self, prompt: str, llm_string: str) -> Any | None:
        cache_path = self._cache_path(prompt, llm_string)
        if not cache_path.exists():
            return None
        with self._lock:
            try:
                with cache_path.open("rb") as handle:
                    return pickle.load(handle)
            except Exception:  # noqa: BLE001 - corrupt cache should not break LLM calls.
                logging.getLogger(__name__).warning("Ignoring corrupt LangChain cache entry: %s", cache_path)
                return None

    def update(self, prompt: str, llm_string: str, return_val: Any) -> None:
        cache_path = self._cache_path(prompt, llm_string)
        with self._lock:
            with tempfile.NamedTemporaryFile("wb", dir=self.path, delete=False) as handle:
                pickle.dump(return_val, handle)
                temp_path = Path(handle.name)
            temp_path.replace(cache_path)

    def clear(self, **kwargs: Any) -> None:
        with self._lock:
            for cache_file in self.path.glob("*.pickle"):
                cache_file.unlink(missing_ok=True)


def configure_llm_cache(settings: dict[str, Any] | None = None) -> StableFileCache | None:
    effective = settings or {}
    if effective.get("cache_enabled", True) is False:
        set_llm_cache(None)
        return None
    cache = StableFileCache(effective.get("cache_path", ".cache/langchain_llm"))
    set_llm_cache(cache)
    return cache
