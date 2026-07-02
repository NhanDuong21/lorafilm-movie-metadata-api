from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PreviewSource(BaseModel):
    provider: str = "TMDB"
    externalId: str
    fetchedAt: datetime


class PreviewGenre(BaseModel):
    code: str
    name: str


class PreviewDirector(BaseModel):
    name: str


class PreviewActor(BaseModel):
    name: str
    character: Optional[str] = None


class PreviewCountry(BaseModel):
    code: str
    name: str


class PreviewMovie(BaseModel):
    title: str
    originalTitle: str
    description: Optional[str] = None
    durationMinutes: Optional[int] = None
    releaseDate: Optional[str] = None
    originalLanguage: Optional[str] = None
    posterUrl: Optional[str] = None
    backdropUrl: Optional[str] = None
    trailerUrl: Optional[str] = None
    genres: List[PreviewGenre] = []
    directors: List[PreviewDirector] = []
    actors: List[PreviewActor] = []
    countries: List[PreviewCountry] = []


class PreviewWarning(BaseModel):
    field: str
    code: str
    message: str


class ImportPreview(BaseModel):
    source: PreviewSource
    movie: PreviewMovie
    warnings: List[PreviewWarning] = []
