from contextlib import asynccontextmanager
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.__engine = create_async_engine(url, echo=echo)
        self.__factory = async_sessionmaker(
            bind=self.__engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @asynccontextmanager
    async def create_session(self) -> AsyncIterable[AsyncSession]:
        async with self.__factory.begin() as session:
            yield session
