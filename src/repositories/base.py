from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Generic, Sequence, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Base
from src.services.dto import AbstractCreateDTO, AbstractUpdateDTO

ModelType = TypeVar("ModelType", bound=Base)
CreateDataType = TypeVar("CreateDataType", bound=AbstractCreateDTO)
UpdateDataType = TypeVar("UpdateDataType", bound=AbstractUpdateDTO)


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

    async def get_list(self, **kwargs) -> Sequence[ModelType]:
        stmt = select(self.model)

        if kwargs:
            for key, value in kwargs.items():
                stmt = stmt.where(getattr(self.model, key) == value)

        return (await self.session.scalars(stmt)).all()

    async def get_by_pk(self, pk: Any) -> ModelType | None:
        return await self.session.get(self.model, pk)

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def get_by_attr(self, attr_name: str, attr_value: Any) -> ModelType | None:
        return await self.session.scalar(
            select(self.model).where(getattr(self.model, attr_name) == attr_value)
        )

    async def update(self, obj: ModelType, dto: UpdateDataType) -> ModelType:
        update_data = asdict(dto)

        for field in jsonable_encoder(obj):
            if update_data.get(field) is not None:
                setattr(obj, field, update_data[field])

        await self.session.flush()
        await self.session.refresh(obj)
        return obj
