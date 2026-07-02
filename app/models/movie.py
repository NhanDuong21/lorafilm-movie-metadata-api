from pydantic import BaseModel
from typing import Optional, List


class Genre(BaseModel):
    externalId: str
    code: str
    name: str
    originalName: str


class ProductionCountry(BaseModel):
    code: str
    name: str


class ProductionCompany(BaseModel):
    externalId: str
    name: str
    logoUrl: Optional[str] = None


class SpokenLanguage(BaseModel):
    code: str
    name: str


class MovieSearchResult(BaseModel):
    provider: str = "TMDB"
    externalId: str
    title: str
    originalTitle: str
    overview: Optional[str] = None
    releaseDate: Optional[str] = None
    releaseYear: Optional[int] = None
    originalLanguage: Optional[str] = None
    posterUrl: Optional[str] = None
    backdropUrl: Optional[str] = None
    adult: bool = False
    popularity: Optional[float] = None
    voteAverage: Optional[float] = None
    voteCount: Optional[int] = None


class MovieDetails(BaseModel):
    provider: str = "TMDB"
    externalId: str
    imdbId: Optional[str] = None
    title: str
    originalTitle: str
    tagline: Optional[str] = None
    overview: Optional[str] = None
    runtimeMinutes: Optional[int] = None
    releaseDate: Optional[str] = None
    releaseYear: Optional[int] = None
    status: Optional[str] = None
    adult: bool = False
    originalLanguage: Optional[str] = None
    spokenLanguages: List[SpokenLanguage] = []
    genres: List[Genre] = []
    productionCountries: List[ProductionCountry] = []
    productionCompanies: List[ProductionCompany] = []
    posterUrl: Optional[str] = None
    backdropUrl: Optional[str] = None
    homepageUrl: Optional[str] = None
    popularity: Optional[float] = None
    voteAverage: Optional[float] = None
    voteCount: Optional[int] = None
