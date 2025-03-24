from contextlib import aclosing, asynccontextmanager
from typing import AsyncIterator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI

from src.api.main_router import main_router
from src.core import get_logger
from src.core.settings import AppSettings, get_settings
from src.infrastructure.di.container import init_container

logger = get_logger(__name__)


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa: ARG001 - required by lifespan protocol
) -> AsyncIterator[None]:
    async with aclosing(init_container()):
        yield


def create_app() -> FastAPI:
    settings: AppSettings = get_settings(AppSettings)
    app = FastAPI(
        lifespan=_lifespan,
        title=settings.title,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(main_router, prefix="/api")
    app.add_middleware(AioInjectMiddleware, container=init_container())

    return app
