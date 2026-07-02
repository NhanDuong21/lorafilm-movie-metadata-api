from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "lorafilm-movie-metadata-api"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8090
    LOG_LEVEL: str = "INFO"

    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p"
    TMDB_BEARER_TOKEN: str = ""
    TMDB_DEFAULT_LANGUAGE: str = "vi-VN"
    TMDB_FALLBACK_LANGUAGE: str = "en-US"
    TMDB_DEFAULT_REGION: str = "VN"

    REDIS_URL: str = "redis://redis:6379/0"
    CACHE_ENABLED: bool = True

    CORS_ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    MAX_CAST_MEMBERS: int = 20
    MAX_POSTERS: int = 10
    MAX_BACKDROPS: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
