from __future__ import annotations

import json
from typing import Any, Callable, TypeVar

from redis import Redis

T = TypeVar("T")


class RedisQueryCache:
    def __init__(self, url: str = "redis://127.0.0.1:6380/2", *, prefix: str = "taskmanagement:query:") -> None:
        self.client = Redis.from_url(url, decode_responses=True, socket_connect_timeout=0.2, socket_timeout=0.5)
        self.prefix = prefix

    def get_or_set(self, key: str, ttl_seconds: int, loader: Callable[[], T]) -> T:
        cache_key = f"{self.prefix}{key}"
        try:
            cached = self.client.get(cache_key)
            if cached is not None:
                return json.loads(cached)
        except Exception:
            return loader()
        value = loader()
        try:
            self.client.setex(cache_key, ttl_seconds, json.dumps(value, ensure_ascii=False, default=str))
        except Exception:
            pass
        return value

    def invalidate_prefix(self, prefix: str = "") -> None:
        pattern = f"{self.prefix}{prefix}*"
        try:
            cursor = 0
            while True:
                cursor, keys = self.client.scan(cursor=cursor, match=pattern, count=100)
                if keys:
                    self.client.delete(*keys)
                if cursor == 0:
                    break
        except Exception:
            pass
