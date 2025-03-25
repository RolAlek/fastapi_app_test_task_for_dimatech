from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Base
from src.services.dto import AbstractCreateDTO

ModelType = TypeVar("ModelType", bound=Base)
CreateDataType = TypeVar("CreateDataType", bound=AbstractCreateDTO)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


@dataclass
class BaseSQLAlchemyRepository(
    Generic[ModelType, CreateDataType],
    AbstractRepository,
):
    session: AsyncSession
    model = None

    async def add(self, data: CreateDataType) -> ModelType:
        instance = self.model(**asdict(data))
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_list(self) -> list[ModelType]:
        return (await self.session.scalars(select(self.model))).all()

    async def get_by_pk(self, pk: Any) -> ModelType | None:
        return await self.session.get(self.model, pk)

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)

    async def get_by_attr(self, attr_name: str, attr_value: Any) -> ModelType | None:
        return await self.session.scalar(
            select(self.model).where(getattr(self.model, attr_name) == attr_value)
        )
