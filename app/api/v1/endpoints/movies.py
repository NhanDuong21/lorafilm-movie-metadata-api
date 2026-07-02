from fastapi import APIRouter, Depends, Query, Path, Response
from typing import Optional
from app.models.common import ApiResponse, PaginatedData
from app.models.movie import MovieSearchResult, MovieDetails
from app.models.credit import MovieCredits
from app.models.video import MovieVideos
from app.models.image import MovieImages
from app.models.import_preview import ImportPreview
from app.services.movie_metadata_service import MovieMetadataService
from app.services.import_preview_service import ImportPreviewService
from app.api.dependencies import get_movie_metadata_service, get_import_preview_service
from app.core.exceptions import ValidationException
from app.core.constants import CacheHeaders

router = APIRouter()


def validate_external_id(external_id: str) -> None:
    if not external_id.isdigit() or int(external_id) <= 0:
        raise ValidationException("Invalid external ID format. Must be a positive integer.")


@router.get("/movies/search", response_model=ApiResponse[PaginatedData[MovieSearchResult]])
async def search_movies(
    response: Response,
    query: str = Query(..., min_length=2, max_length=200),
    page: int = Query(1, ge=1),
    language: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    includeAdult: bool = Query(False),
    service: MovieMetadataService = Depends(get_movie_metadata_service),
) -> ApiResponse[PaginatedData[MovieSearchResult]]:
    query_clean = query.strip()
    if len(query_clean) < 2:
        raise ValidationException("Query must be at least 2 characters long")

    data, cache_status = await service.search_movies(
        query_clean, page, language, region, includeAdult
    )
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(success=True, message="Movies retrieved successfully", data=data)


@router.get("/movies/{externalId}", response_model=ApiResponse[MovieDetails])
async def get_movie_details(
    response: Response,
    externalId: str = Path(...),
    language: Optional[str] = Query(None),
    service: MovieMetadataService = Depends(get_movie_metadata_service),
) -> ApiResponse[MovieDetails]:
    validate_external_id(externalId)
    data, cache_status = await service.get_movie_details(externalId, language)
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(success=True, message="Movie details retrieved successfully", data=data)


@router.get("/movies/{externalId}/credits", response_model=ApiResponse[MovieCredits])
async def get_movie_credits(
    response: Response,
    externalId: str = Path(...),
    language: Optional[str] = Query(None),
    service: MovieMetadataService = Depends(get_movie_metadata_service),
) -> ApiResponse[MovieCredits]:
    validate_external_id(externalId)
    data, cache_status = await service.get_movie_credits(externalId, language)
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(success=True, message="Movie credits retrieved successfully", data=data)


@router.get("/movies/{externalId}/videos", response_model=ApiResponse[MovieVideos])
async def get_movie_videos(
    response: Response,
    externalId: str = Path(...),
    language: Optional[str] = Query(None),
    service: MovieMetadataService = Depends(get_movie_metadata_service),
) -> ApiResponse[MovieVideos]:
    validate_external_id(externalId)
    data, cache_status = await service.get_movie_videos(externalId, language)
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(success=True, message="Movie videos retrieved successfully", data=data)


@router.get("/movies/{externalId}/images", response_model=ApiResponse[MovieImages])
async def get_movie_images(
    response: Response,
    externalId: str = Path(...),
    language: Optional[str] = Query(None),
    service: MovieMetadataService = Depends(get_movie_metadata_service),
) -> ApiResponse[MovieImages]:
    validate_external_id(externalId)
    data, cache_status = await service.get_movie_images(externalId, language)
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(success=True, message="Movie images retrieved successfully", data=data)


@router.get("/movies/{externalId}/import-preview", response_model=ApiResponse[ImportPreview])
async def get_import_preview(
    response: Response,
    externalId: str = Path(...),
    language: Optional[str] = Query(None),
    service: ImportPreviewService = Depends(get_import_preview_service),
) -> ApiResponse[ImportPreview]:
    validate_external_id(externalId)
    data, cache_status = await service.get_import_preview(externalId, language)
    response.headers[CacheHeaders.STATUS] = cache_status

    return ApiResponse(
        success=True, message="Movie import preview generated successfully", data=data
    )
