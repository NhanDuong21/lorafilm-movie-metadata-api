import httpx
from typing import Any, Dict, Optional
from app.core.config import settings
from app.core.exceptions import ProviderException, ResourceNotFoundException
import logging
from httpx import HTTPStatusError, RequestError

logger = logging.getLogger(__name__)


class TMDBClient:
    def __init__(self) -> None:
        if not settings.TMDB_BEARER_TOKEN:
            logger.error("TMDB_BEARER_TOKEN is not configured")

        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}",
            "Accept": "application/json",
        }

        self.client = httpx.AsyncClient(
            base_url=settings.TMDB_BASE_URL,
            headers=self.headers,
            timeout=httpx.Timeout(connect=3.0, read=10.0, write=5.0, pool=5.0),
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def _request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        if not settings.TMDB_BEARER_TOKEN:
            raise ProviderException("TMDB is not configured", "TMDB_NOT_CONFIGURED", 500)

        try:
            response = await self.client.request(method, endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            status = e.response.status_code
            if status == 401:
                raise ProviderException("Unauthorized by provider", "PROVIDER_UNAUTHORIZED", 502)
            elif status == 404:
                raise ResourceNotFoundException("Movie not found", "MOVIE_NOT_FOUND", 404)
            elif status == 429:
                raise ProviderException("Provider rate limited", "PROVIDER_RATE_LIMITED", 429)
            elif status in (502, 503):
                raise ProviderException("Provider unavailable", "PROVIDER_UNAVAILABLE", 503)
            elif status == 504:
                raise ProviderException("Provider timeout", "PROVIDER_TIMEOUT", 504)

            logger.error(f"Provider error: {status}")
            raise ProviderException(f"Provider error {status}", "PROVIDER_ERROR", 502)
        except httpx.ReadTimeout:
            raise ProviderException("Provider read timeout", "PROVIDER_TIMEOUT", 504)
        except RequestError as e:
            logger.error(f"Provider connection error: {e}")
            raise ProviderException("Provider unavailable", "PROVIDER_UNAVAILABLE", 503)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", endpoint, params)
