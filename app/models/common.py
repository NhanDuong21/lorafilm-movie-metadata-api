from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    errorCode: Optional[str] = None
    data: Optional[T] = None


class PaginatedData(BaseModel, Generic[T]):
    query: Optional[str] = None
    page: int
    totalPages: int
    totalResults: int
    results: list[T]
