from typing import Protocol, Optional
from app.models.movie import MovieSearchResult, MovieDetails
from app.models.credit import MovieCredits
from app.models.video import MovieVideos
from app.models.image import MovieImages
from app.models.common import PaginatedData


class MovieMetadataProvider(Protocol):
    async def search_movies(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
        include_adult: bool = False,
    ) -> PaginatedData[MovieSearchResult]: ...

    async def get_movie_details(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieDetails: ...

    async def get_movie_credits(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieCredits: ...

    async def get_movie_videos(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieVideos: ...

    async def get_movie_images(
        self, external_id: str, language: Optional[str] = None
    ) -> MovieImages: ...
