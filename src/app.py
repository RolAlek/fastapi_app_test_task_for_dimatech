from contextlib import aclosing, asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from core import get_logger, settings
from core.di.container import create_container

logger = get_logger(__name__)


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa: ARG001 - required by lifespan protocol
) -> AsyncIterator[None]:
    async with aclosing(create_container()):
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
        title=settings.app.title,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    return app
