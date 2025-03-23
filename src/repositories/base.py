from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.dto import AbstractCreateDTO
from src.database.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
DataType = TypeVar("DataType", bound=AbstractCreateDTO)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


@dataclass
class BaseSQLAlchemyRepository(AbstractRepository):
    session: AsyncSession
    model: ModelType = None

    async def add(self, data: DataType) -> ModelType:
        instance = self.model(**asdict(data))
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_list(self) -> list[ModelType]:
        return (await self.session.scalars(select(self.model))).all()
