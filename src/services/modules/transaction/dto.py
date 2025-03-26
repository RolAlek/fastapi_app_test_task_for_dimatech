from dataclasses import dataclass

from src.services.dto import AbstractCreateDTO


@dataclass
class CreateTransactionDto(AbstractCreateDTO):
    oid: str
    amount: float
    account_oid: int
