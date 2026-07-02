from typing import Optional
from app.providers.base import MovieMetadataProvider
from app.providers.tmdb.client import TMDBClient
from app.providers.tmdb.models import (
    TMDBSearchResponse,
    TMDBMovieDetailsResponse,
    TMDBCreditsResponse,
    TMDBVideosResponse,
    TMDBImagesResponse,
)
from app.providers.tmdb.mapper import TMDBMapper
from app.models.movie import MovieSearchResult, MovieDetails
from app.models.credit import MovieCredits
from app.models.video import MovieVideos
from app.models.image import MovieImages
from app.models.common import PaginatedData
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TMDBProvider(MovieMetadataProvider):
    def __init__(self, client: TMDBClient):
        self.client = client

    def _get_lang(self, language: Optional[str]) -> str:
        return language or settings.TMDB_DEFAULT_LANGUAGE

    def _get_region(self, region: Optional[str]) -> str:
        return region or settings.TMDB_DEFAULT_REGION

    async def search_movies(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
        include_adult: bool = False,
    ) -> PaginatedData[MovieSearchResult]:
        params = {
            "query": query,
            "page": page,
            "language": self._get_lang(language),
            "region": self._get_region(region),
            "include_adult": "true" if include_adult else "false",
        }
        raw_data = await self.client.get("/search/movie", params)
        response_model = TMDBSearchResponse.model_validate(raw_data)
        return TMDBMapper.map_search_response(query, response_model)

    async def get_movie_details(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieDetails:
        lang = self._get_lang(language)
        params = {"language": lang}
        raw_data = await self.client.get(f"/movie/{external_id}", params)
        response_model = TMDBMovieDetailsResponse.model_validate(raw_data)

        # Fallback for empty overview
        if not response_model.overview and lang != settings.TMDB_FALLBACK_LANGUAGE:
            fallback_params = {"language": settings.TMDB_FALLBACK_LANGUAGE}
            fallback_raw = await self.client.get(f"/movie/{external_id}", fallback_params)
            fallback_model = TMDBMovieDetailsResponse.model_validate(fallback_raw)
            if fallback_model.overview:
                response_model.overview = fallback_model.overview

        return TMDBMapper.map_movie_details(response_model)

    async def get_movie_credits(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieCredits:
        params = {"language": self._get_lang(language)}
        raw_data = await self.client.get(f"/movie/{external_id}/credits", params)
        response_model = TMDBCreditsResponse.model_validate(raw_data)
        return TMDBMapper.map_credits(response_model)

    async def get_movie_videos(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieVideos:
        params = {"language": self._get_lang(language)}
        raw_data = await self.client.get(f"/movie/{external_id}/videos", params)
        response_model = TMDBVideosResponse.model_validate(raw_data)
        return TMDBMapper.map_videos(response_model)

    async def get_movie_images(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieImages:
        # For images, TMDB sometimes requires omitting language or passing include_image_language to get all
        # We fetch without strict language filter to get backdrops correctly and filter in mapper
        params = {
            "include_image_language": f"{self._get_lang(language)},{settings.TMDB_FALLBACK_LANGUAGE},null"
        }
        raw_data = await self.client.get(f"/movie/{external_id}/images", params)
        response_model = TMDBImagesResponse.model_validate(raw_data)
        return TMDBMapper.map_images(response_model)
