from pydantic import BaseModel
from typing import Optional, List


class Image(BaseModel):
    filePath: str
    urlOriginal: str
    urlW500: Optional[str] = None
    urlW1280: Optional[str] = None
    width: int
    height: int
    aspectRatio: float
    language: Optional[str] = None
    voteAverage: float
    voteCount: int


class MovieImages(BaseModel):
    posters: List[Image]
    backdrops: List[Image]
