import pytest
import respx
from httpx import Response
from app.core.config import settings

@pytest.mark.asyncio
@respx.mock
async def test_get_movie_credits(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1/credits").mock(return_value=Response(200, json={
        "id": 1,
        "cast": [{"id": 10, "name": "Actor A", "order": 0}],
        "crew": [{"id": 20, "name": "Director A", "job": "Director"}]
    }))
    
    response = await async_client.get("/api/v1/movies/1/credits")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["directors"]) == 1
    assert data["data"]["directors"][0]["name"] == "Director A"

@pytest.mark.asyncio
@respx.mock
async def test_get_movie_videos(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1/videos").mock(return_value=Response(200, json={
        "id": 1,
        "results": [
            {"id": "v1", "key": "key1", "name": "Trailer", "site": "YouTube", "type": "Trailer", "official": True, "iso_639_1": "en"}
        ]
    }))
    
    response = await async_client.get("/api/v1/movies/1/videos")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["trailers"]) == 1
    assert data["data"]["preferredTrailer"]["externalId"] == "v1"

@pytest.mark.asyncio
@respx.mock
async def test_get_movie_images(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1/images").mock(return_value=Response(200, json={
        "id": 1,
        "posters": [
            {"file_path": "/p1.jpg", "width": 500, "height": 750, "aspect_ratio": 0.66, "vote_average": 5, "vote_count": 10}
        ],
        "backdrops": []
    }))
    
    response = await async_client.get("/api/v1/movies/1/images")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["posters"]) == 1

@pytest.mark.asyncio
@respx.mock
async def test_get_import_preview(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1").mock(return_value=Response(200, json={
        "id": 1,
        "title": "Test",
        "original_title": "Test",
        "overview": "Overview",
        "genres": [{"id": 28, "name": "Action"}],
        "production_countries": [],
        "production_companies": [],
        "spoken_languages": []
    }))
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1/credits").mock(return_value=Response(200, json={
        "id": 1, "cast": [], "crew": []
    }))
    respx.get(f"{settings.TMDB_BASE_URL}/movie/1/videos").mock(return_value=Response(200, json={
        "id": 1, "results": []
    }))
    
    response = await async_client.get("/api/v1/movies/1/import-preview")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["movie"]["title"] == "Test"
    assert len(data["data"]["warnings"]) > 0

@pytest.mark.asyncio
@respx.mock
async def test_provider_errors(async_client):
    respx.get(f"{settings.TMDB_BASE_URL}/movie/2").mock(return_value=Response(401))
    response = await async_client.get("/api/v1/movies/2")
    assert response.status_code == 502
    assert response.json()["errorCode"] == "PROVIDER_UNAUTHORIZED"
    
    respx.get(f"{settings.TMDB_BASE_URL}/movie/3").mock(return_value=Response(429))
    response = await async_client.get("/api/v1/movies/3")
    assert response.status_code == 429
    assert response.json()["errorCode"] == "PROVIDER_RATE_LIMITED"
    
    respx.get(f"{settings.TMDB_BASE_URL}/movie/4").mock(return_value=Response(500))
    response = await async_client.get("/api/v1/movies/4")
    assert response.status_code == 502
    assert response.json()["errorCode"] == "PROVIDER_ERROR"
