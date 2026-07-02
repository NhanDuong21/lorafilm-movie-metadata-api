from pydantic import BaseModel
from typing import Optional, List


class Trailer(BaseModel):
    externalId: str
    name: str
    platform: str
    type: str
    official: bool
    language: Optional[str] = None
    publishedAt: Optional[str] = None
    url: str


class MovieVideos(BaseModel):
    trailers: List[Trailer]
    preferredTrailer: Optional[Trailer] = None
