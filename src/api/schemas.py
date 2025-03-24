from typing import Iterable, Self

from pydantic import BaseModel, ConfigDict

from src.repositories.base import ModelType


def snake_to_camel(field_name: str) -> str:
    first, *rest = field_name.split("_")
    return first + "".join(map(str.capitalize, rest))


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=snake_to_camel,
    )

    @classmethod
    def model_validate_list(cls, entities: Iterable[ModelType]) -> list[Self]:
        return [cls.model_validate(entity) for entity in entities]
