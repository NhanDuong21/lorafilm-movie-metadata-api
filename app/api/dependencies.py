from app.providers.tmdb.client import TMDBClient
from app.providers.tmdb.provider import TMDBProvider
from app.providers.base import MovieMetadataProvider
from app.cache.base import CacheClient
from app.cache.redis_cache import RedisCache
from app.cache.memory_cache import MemoryCache
from app.repositories.cache_repository import CacheRepository
from app.services.movie_metadata_service import MovieMetadataService
from app.services.import_preview_service import ImportPreviewService
import logging

logger = logging.getLogger(__name__)

# Global instances
_cache_client: CacheClient | None = None
_tmdb_client: TMDBClient | None = None


async def init_dependencies() -> None:
    global _cache_client, _tmdb_client

    # Initialize cache
    redis = RedisCache()
    if await redis.is_healthy():
        logger.info("Using Redis cache")
        _cache_client = redis
    else:
        logger.warning("Redis is unavailable, falling back to Memory cache")
        _cache_client = MemoryCache()

    # Initialize TMDB client
    _tmdb_client = TMDBClient()


async def close_dependencies() -> None:
    global _cache_client, _tmdb_client
    if _cache_client:
        await _cache_client.close()
    if _tmdb_client:
        await _tmdb_client.close()


def get_cache_repository() -> CacheRepository:
    if not _cache_client:
        raise RuntimeError("Cache client not initialized")
    return CacheRepository(_cache_client)


def get_provider() -> MovieMetadataProvider:
    if not _tmdb_client:
        raise RuntimeError("TMDB client not initialized")
    return TMDBProvider(_tmdb_client)


def get_movie_metadata_service() -> MovieMetadataService:
    return MovieMetadataService(get_provider(), get_cache_repository())


def get_import_preview_service() -> ImportPreviewService:
    return ImportPreviewService(get_movie_metadata_service(), get_cache_repository())
