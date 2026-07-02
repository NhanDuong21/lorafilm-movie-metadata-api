import pytest
import respx
from httpx import Response
from app.core.config import settings


@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["UP", "DEGRADED"]
    assert data["service"] == settings.APP_NAME


@pytest.mark.asyncio
@respx.mock
async def test_search_movies(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/search/movie").mock(
        return_value=Response(
            200,
            json={
                "page": 1,
                "total_pages": 1,
                "total_results": 1,
                "results": [
                    {"id": 1, "title": "Test Movie", "original_title": "Test Movie", "adult": False}
                ],
            },
        )
    )

    response = await async_client.get("/api/v1/movies/search?query=test")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["totalResults"] == 1
    assert data["data"]["results"][0]["title"] == "Test Movie"


@pytest.mark.asyncio
@respx.mock
async def test_get_movie_details(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1").mock(
        return_value=Response(
            200,
            json={
                "id": 1,
                "title": "Test Movie",
                "original_title": "Test Movie",
                "adult": False,
                "genres": [],
                "production_countries": [],
                "production_companies": [],
                "spoken_languages": [],
            },
        )
    )

    response = await async_client.get("/api/v1/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Movie"


@pytest.mark.asyncio
@respx.mock
async def test_get_movie_details_not_found(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/999").mock(
        return_value=Response(
            404, json={"status_message": "The resource you requested could not be found."}
        )
    )

    response = await async_client.get("/api/v1/movies/999")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["errorCode"] == "MOVIE_NOT_FOUND"


@pytest.mark.asyncio
async def test_invalid_external_id(async_client):
    response = await async_client.get("/api/v1/movies/-1")
    assert response.status_code == 400
    data = response.json()
    assert data["errorCode"] == "VALIDATION_ERROR"
