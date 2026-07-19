from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from backend.src.api.routes.password import router as password_router
from backend.src.core.config import get_settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.http_client = httpx.AsyncClient(
        timeout=5.0,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    yield
    await application.state.http_client.aclose()


def create_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        lifespan=lifespan,
    )

    application.add_middleware(GZipMiddleware, minimum_size=1000)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=["*"],
        max_age=86400,
    )

    application.include_router(password_router)

    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        timeout_keep_alive=5,
    )
