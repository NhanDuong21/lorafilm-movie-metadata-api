from typing import Optional, Any
import json
import logging
from pydantic import BaseModel
from app.cache.base import CacheClient

logger = logging.getLogger(__name__)


class CacheRepository:
    def __init__(self, cache_client: CacheClient):
        self.cache_client = cache_client

    async def get(self, key: str) -> Optional[Any]:
        try:
            val = await self.cache_client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Error parsing cache for {key}: {e}")
        return None

    async def set(self, key: str, value: BaseModel, ttl: int) -> None:
        try:
            val_str = value.model_dump_json()
            await self.cache_client.set(key, val_str, ttl)
        except Exception as e:
            logger.warning(f"Error setting cache for {key}: {e}")

    async def is_healthy(self) -> bool:
        return await self.cache_client.is_healthy()
