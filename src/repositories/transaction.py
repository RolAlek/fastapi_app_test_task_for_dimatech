from dataclasses import dataclass

from sqlalchemy import exists, select

from src.infrastructure.database.models import Transaction
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
