from dataclasses import dataclass

from src.services.dto import AbstractCreateDTO


@dataclass
class CreateTokenDTO(AbstractCreateDTO):
    token: str
    user_id: int


@dataclass
class UpdateTokenDTO(AbstractCreateDTO):
    token: str
