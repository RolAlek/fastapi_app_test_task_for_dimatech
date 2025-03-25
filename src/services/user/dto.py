from dataclasses import dataclass
from typing import Optional

from src.services.dto import AbstractCreateDTO, AbstractUpdateDTO


@dataclass
class UserCreateDTO(AbstractCreateDTO):
    email: str
    hashed_password: str
    first_name: str
    last_name: str


@dataclass
class UserUpdateDTO(AbstractUpdateDTO):
    email: Optional[str]
    hashed_password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: Optional[bool]
