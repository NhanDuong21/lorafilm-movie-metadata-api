import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.api.dependencies import init_dependencies, close_dependencies
from app.core.config import settings


@pytest.fixture(autouse=True)
async def setup_dependencies():
    await init_dependencies()
    yield
    await close_dependencies()


@pytest.fixture
async def async_client():
    settings.TMDB_BEARER_TOKEN = "mock_token"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
