from pydantic import BaseModel
from typing import Optional, List


class Director(BaseModel):
    externalId: str
    name: str
    profileUrl: Optional[str] = None


class CastMember(BaseModel):
    externalId: str
    name: str
    character: Optional[str] = None
    order: int
    profileUrl: Optional[str] = None


class MovieCredits(BaseModel):
    directors: List[Director]
    cast: List[CastMember]
