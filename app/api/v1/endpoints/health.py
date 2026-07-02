from fastapi import APIRouter, Depends, Response
from typing import Dict, Any
from app.api.dependencies import get_cache_repository
from app.repositories.cache_repository import CacheRepository
from app.core.config import settings
from app.cache.redis_cache import RedisCache

router = APIRouter()


@router.get("/health")
async def health_check(
    response: Response, cache: CacheRepository = Depends(get_cache_repository)
) -> Dict[str, Any]:
    redis_up = False

    # Check if the cache client is actually redis and healthy
    if isinstance(cache.cache_client, RedisCache):
        redis_up = await cache.is_healthy()

    status = "UP" if redis_up or not settings.CACHE_ENABLED else "DEGRADED"

    tmdb_status = "CONFIGURED" if settings.TMDB_BEARER_TOKEN else "MISSING"

    return {
        "status": status,
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "dependencies": {"redis": "UP" if redis_up else "DOWN", "tmdb": tmdb_status},
    }
