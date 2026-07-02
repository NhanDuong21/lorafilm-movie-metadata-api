from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import ApiException
from app.models.common import ApiResponse
import logging

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiException)
    async def api_exception_handler(request: Request, exc: ApiException) -> JSONResponse:
        content = ApiResponse(
            success=False, message=exc.message, errorCode=exc.error_code
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        content = ApiResponse(
            success=False, message="Invalid request parameters", errorCode="VALIDATION_ERROR"
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=400, content=content)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        content = ApiResponse(
            success=False, message="Internal server error", errorCode="INTERNAL_SERVER_ERROR"
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=500, content=content)
