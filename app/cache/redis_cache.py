from typing import Optional
from app.cache.base import CacheClient
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisCache(CacheClient):
    def __init__(self) -> None:
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.warning(f"Redis get error: {e}")
            return None

    async def set(self, key: str, value: str, ttl_seconds: int) -> None:
        try:
            await self.redis.setex(key, ttl_seconds, value)
        except Exception as e:
            logger.warning(f"Redis set error: {e}")

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.warning(f"Redis delete error: {e}")

    async def is_healthy(self) -> bool:
        try:
            return await self.redis.ping()
        except Exception:
            return False

    async def close(self) -> None:
        await self.redis.close()
