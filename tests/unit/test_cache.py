import pytest
import asyncio
from app.cache.memory_cache import MemoryCache
from app.cache.redis_cache import RedisCache
from app.repositories.cache_repository import CacheRepository
from pydantic import BaseModel

class DummyModel(BaseModel):
    name: str

@pytest.mark.asyncio
async def test_memory_cache():
    cache = MemoryCache()
    await cache.set("key1", "val1", 1)
    val = await cache.get("key1")
    assert val == "val1"
    
    await cache.delete("key1")
    val2 = await cache.get("key1")
    assert val2 is None
    
    await cache.set("key2", "val2", -1)
    val3 = await cache.get("key2")
    assert val3 is None
    
    assert await cache.is_healthy() is True
    await cache.close()

@pytest.mark.asyncio
async def test_cache_repository():
    cache_client = MemoryCache()
    repo = CacheRepository(cache_client)
    
    model = DummyModel(name="test")
    await repo.set("m1", model, 10)
    
    res = await repo.get("m1")
    assert res is not None
    assert res["name"] == "test"
    
    res2 = await repo.get("missing")
    assert res2 is None
    
    assert await repo.is_healthy() is True
