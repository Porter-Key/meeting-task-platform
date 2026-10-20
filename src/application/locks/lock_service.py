from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from typing import Any, Iterator

from redis import Redis


class LockService:
    def __init__(self, lock_url: str) -> None:
        self.client = Redis.from_url(lock_url, decode_responses=True, socket_connect_timeout=0.5, socket_timeout=0.5)

    def _release_script(self, lock_key: str, token: str) -> int:
        return int(
            self.client.eval(
                """
                if redis.call('GET', KEYS[1]) == ARGV[1] then
                    return redis.call('DEL', KEYS[1])
                end
                return 0
                """,
                1,
                lock_key,
                token,
            )
        )

    @contextmanager
    def acquire(self, lock_key: str, *, ttl_seconds: int = 3600, metadata: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        owner_id = uuid.uuid4().hex
        token = uuid.uuid4().hex
        acquired = bool(self.client.set(lock_key, token, nx=True, ex=ttl_seconds))
        result: dict[str, Any] = {"acquired": acquired, "lock_key": lock_key, "owner_id": owner_id, "token": token, "metadata": metadata or {}}
        if acquired:
            result["expires_at"] = datetime.now(UTC) + timedelta(seconds=ttl_seconds)
        try:
            yield result
        finally:
            if acquired:
                self._release_script(lock_key, token)
