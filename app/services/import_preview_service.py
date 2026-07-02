from typing import Optional, Tuple
import asyncio
from datetime import datetime, timezone
from app.services.movie_metadata_service import MovieMetadataService
from app.repositories.cache_repository import CacheRepository
from app.models.import_preview import (
    ImportPreview,
    PreviewSource,
    PreviewMovie,
    PreviewGenre,
    PreviewDirector,
    PreviewActor,
    PreviewCountry,
    PreviewWarning,
)
from app.core.config import settings


class ImportPreviewService:
    def __init__(self, metadata_service: MovieMetadataService, cache: CacheRepository):
        self.metadata_service = metadata_service
        self.cache = cache

    async def get_import_preview(
        self, external_id: str, language: Optional[str] = None
    ) -> Tuple[ImportPreview, str]:
        lang = language or settings.TMDB_DEFAULT_LANGUAGE
        cache_key = f"movie-metadata:v1:import-preview:{lang}:{external_id}"

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                return ImportPreview.model_validate(cached), "HIT"

        # Concurrently fetch required data
        details_task = self.metadata_service.get_movie_details(external_id, language)
        credits_task = self.metadata_service.get_movie_credits(external_id, language)
        videos_task = self.metadata_service.get_movie_videos(external_id, language)

        (details, _), (credits, _), (videos, _) = await asyncio.gather(
            details_task, credits_task, videos_task
        )

        warnings = []
        warnings.append(
            PreviewWarning(
                field="ageRating",
                code="NOT_PROVIDED",
                message="Age rating must be configured by the LoraFilm administrator.",
            )
        )
        warnings.append(
            PreviewWarning(
                field="status",
                code="NOT_PROVIDED",
                message="Internal status must be configured by the LoraFilm administrator.",
            )
        )
        warnings.append(
            PreviewWarning(
                field="ticketPrice",
                code="NOT_PROVIDED",
                message="Ticket price must be configured by the LoraFilm administrator.",
            )
        )

        preview = ImportPreview(
            source=PreviewSource(
                provider="TMDB", externalId=external_id, fetchedAt=datetime.now(timezone.utc)
            ),
            movie=PreviewMovie(
                title=details.title,
                originalTitle=details.originalTitle,
                description=details.overview,
                durationMinutes=details.runtimeMinutes,
                releaseDate=details.releaseDate,
                originalLanguage=details.originalLanguage,
                posterUrl=details.posterUrl,
                backdropUrl=details.backdropUrl,
                trailerUrl=videos.preferredTrailer.url if videos.preferredTrailer else None,
                genres=[PreviewGenre(code=g.code, name=g.name) for g in details.genres],
                directors=[PreviewDirector(name=d.name) for d in credits.directors],
                actors=[PreviewActor(name=a.name, character=a.character) for a in credits.cast],
                countries=[
                    PreviewCountry(code=c.code, name=c.name) for c in details.productionCountries
                ],
            ),
            warnings=warnings,
        )

        if settings.CACHE_ENABLED:
            await self.cache.set(cache_key, preview, 21600)  # 6 hours

        return preview, "MISS"
