from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import exists, select

from src.infrastructure.database.models import Account, Transaction
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.modules.transaction.dto import CreateTransactionDto


@dataclass
class _TransactionRepository(
    BaseSQLAlchemyRepository[Transaction, CreateTransactionDto]
):
    model = Transaction

    async def check_exists(self, oid: str):
        return await self.session.scalar(
            select(exists(self.model.oid)).where(self.model.oid == oid)
        )

    async def get_all_for_user(self, user_oid: int) -> Sequence[Transaction]:
        result = await self.session.scalars(
            select(self.model).join(Account).where(Account.user_oid == user_oid)
        )
        return result.all()
