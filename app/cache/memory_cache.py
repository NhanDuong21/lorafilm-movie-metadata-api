from typing import Optional, Dict, Tuple
from app.cache.base import CacheClient
import time
import asyncio


class MemoryCache(CacheClient):
    def __init__(self) -> None:
        self._cache: Dict[str, Tuple[str, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[str]:
        async with self._lock:
            if key in self._cache:
                value, expire_at = self._cache[key]
                if time.time() < expire_at:
                    return value
                else:
                    del self._cache[key]
        return None

    async def set(self, key: str, value: str, ttl_seconds: int) -> None:
        async with self._lock:
            expire_at = time.time() + ttl_seconds
            self._cache[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def is_healthy(self) -> bool:
        return True

    async def close(self) -> None:
        self._cache.clear()
