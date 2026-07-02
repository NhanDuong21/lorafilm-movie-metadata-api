from typing import Optional, Tuple
from app.providers.base import MovieMetadataProvider
from app.repositories.cache_repository import CacheRepository
from app.models.movie import MovieSearchResult, MovieDetails
from app.models.credit import MovieCredits
from app.models.video import MovieVideos
from app.models.image import MovieImages
from app.models.common import PaginatedData
from app.core.config import settings
import hashlib


class MovieMetadataService:
    def __init__(self, provider: MovieMetadataProvider, cache: CacheRepository):
        self.provider = provider
        self.cache = cache

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.encode("utf-8")).hexdigest()

    async def search_movies(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
        include_adult: bool = False,
    ) -> Tuple[PaginatedData[MovieSearchResult], str]:
        lang = language or settings.TMDB_DEFAULT_LANGUAGE
        reg = region or settings.TMDB_DEFAULT_REGION
        query_hash = self._hash_query(query)
        cache_key = f"movie-metadata:v1:search:{lang}:{reg}:{page}:{query_hash}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                # We need to reconstruct the generic model
                return PaginatedData[MovieSearchResult].model_validate(cached), "HIT"

        data = await self.provider.search_movies(query, page, language, region, include_adult)

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, data, 3600)  # 1 hour

        return data, "MISS"

    async def get_movie_details(
        self, external_id: str, language: Optional[str] = None
    ) -> Tuple[MovieDetails, str]:
        lang = language or settings.TMDB_DEFAULT_LANGUAGE
        cache_key = f"movie-metadata:v1:details:{lang}:{external_id}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                return MovieDetails.model_validate(cached), "HIT"

        data = await self.provider.get_movie_details(external_id, language)

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, data, 86400)  # 24 hours

        return data, "MISS"

    async def get_movie_credits(
        self, external_id: str, language: Optional[str] = None
    ) -> Tuple[MovieCredits, str]:
        lang = language or settings.TMDB_DEFAULT_LANGUAGE
        cache_key = f"movie-metadata:v1:credits:{lang}:{external_id}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                return MovieCredits.model_validate(cached), "HIT"

        data = await self.provider.get_movie_credits(external_id, language)

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, data, 86400)  # 24 hours

        return data, "MISS"

    async def get_movie_videos(
        self, external_id: str, language: Optional[str] = None
    ) -> Tuple[MovieVideos, str]:
        lang = language or settings.TMDB_DEFAULT_LANGUAGE
        cache_key = f"movie-metadata:v1:videos:{lang}:{external_id}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                return MovieVideos.model_validate(cached), "HIT"

        data = await self.provider.get_movie_videos(external_id, language)

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, data, 21600)  # 6 hours

        return data, "MISS"

    async def get_movie_images(
        self, external_id: str, language: Optional[str] = None
    ) -> Tuple[MovieImages, str]:
        # Image key doesn't need language as much, since we fetch multiple langs, but let's keep it consistent
        cache_key = f"movie-metadata:v1:images:{external_id}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                return MovieImages.model_validate(cached), "HIT"

        data = await self.provider.get_movie_images(external_id, language)

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, data, 86400)  # 24 hours

        return data, "MISS"
