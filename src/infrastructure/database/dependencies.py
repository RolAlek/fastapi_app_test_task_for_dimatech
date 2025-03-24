from contextlib import asynccontextmanager
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.engine import async_session_factory


@asynccontextmanager
async def create_session() -> AsyncIterable[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session
