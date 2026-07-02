from app.core.config import settings


def build_image_url(path: str | None, size: str = "original") -> str | None:
    if not path:
        return None

    if not path.startswith("/"):
        path = "/" + path

    return f"{settings.TMDB_IMAGE_BASE_URL}/{size}{path}"
