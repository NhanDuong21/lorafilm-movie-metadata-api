from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
import uuid

from app.api.v1.router import router as v1_router
from app.api.dependencies import init_dependencies, close_dependencies
from app.api.exception_handlers import add_exception_handlers
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_dependencies()
    yield
    await close_dependencies()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="LoraFilm Movie Metadata API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next: Any) -> Response:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


add_exception_handlers(app)

app.include_router(v1_router, prefix="/api/v1")
