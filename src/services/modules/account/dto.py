from dataclasses import dataclass

from src.services.dto import AbstractCreateDTO


@dataclass
class CreateAccountDTO(AbstractCreateDTO):
    oid: int
    user_id: int
