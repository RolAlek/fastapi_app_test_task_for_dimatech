from dataclasses import dataclass

from infrastructure.database.models.account import Account
from src.repositories.account import _AccountRepository
from src.services.account.dto import CreateAccountDTO
from src.services.transaction.service import TransactionService
from src.services.user.service import UserService


@dataclass
class AccountService:
    transaction_service: TransactionService
    account_repository: _AccountRepository
    user_service: UserService

    async def add_account(self, dto: CreateAccountDTO) -> Account:
        account = await self.account_repository.add(dto)

        return account
