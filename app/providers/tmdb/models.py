from pydantic import BaseModel
from typing import List, Optional


class TMDBMovieResult(BaseModel):
    id: int
    title: str
    original_title: str
    overview: Optional[str] = None
    release_date: Optional[str] = None
    original_language: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    adult: bool = False
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None


class TMDBSearchResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results: List[TMDBMovieResult]


class TMDBGenre(BaseModel):
    id: int
    name: str


class TMDBProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class TMDBProductionCompany(BaseModel):
    id: int
    name: str
    logo_path: Optional[str] = None


class TMDBSpokenLanguage(BaseModel):
    iso_639_1: str
    name: str


class TMDBMovieDetailsResponse(BaseModel):
    id: int
    imdb_id: Optional[str] = None
    title: str
    original_title: str
    tagline: Optional[str] = None
    overview: Optional[str] = None
    runtime: Optional[int] = None
    release_date: Optional[str] = None
    status: Optional[str] = None
    adult: bool = False
    original_language: Optional[str] = None
    spoken_languages: List[TMDBSpokenLanguage] = []
    genres: List[TMDBGenre] = []
    production_countries: List[TMDBProductionCountry] = []
    production_companies: List[TMDBProductionCompany] = []
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    homepage: Optional[str] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None


class TMDBCastMember(BaseModel):
    id: int
    name: str
    character: Optional[str] = None
    order: int
    profile_path: Optional[str] = None


class TMDBCrewMember(BaseModel):
    id: int
    name: str
    job: str
    profile_path: Optional[str] = None


class TMDBCreditsResponse(BaseModel):
    cast: List[TMDBCastMember] = []
    crew: List[TMDBCrewMember] = []


class TMDBVideo(BaseModel):
    id: str
    name: str
    site: str
    type: str
    official: bool
    iso_639_1: Optional[str] = None
    published_at: Optional[str] = None
    key: str


class TMDBVideosResponse(BaseModel):
    results: List[TMDBVideo] = []


class TMDBImage(BaseModel):
    file_path: str
    width: int
    height: int
    aspect_ratio: float
    iso_639_1: Optional[str] = None
    vote_average: float
    vote_count: int


class TMDBImagesResponse(BaseModel):
    posters: List[TMDBImage] = []
    backdrops: List[TMDBImage] = []
