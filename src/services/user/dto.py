from dataclasses import dataclass

from src.services.dto import AbstractCreateDTO


@dataclass
class UserCreateDTO(AbstractCreateDTO):
    email: str
    hashed_password: str
    first_name: str
    last_name: str
