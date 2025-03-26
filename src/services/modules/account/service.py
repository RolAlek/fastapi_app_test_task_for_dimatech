from dataclasses import dataclass

from src.infrastructure.database.models.account import Account
from src.repositories.account import _AccountRepository
from src.services.modules.account.dto import CreateAccountDTO


@dataclass
class AccountService:
    account_repository: _AccountRepository

    async def add_account(self, dto: CreateAccountDTO) -> Account:
        account = await self.account_repository.add(dto)

        return account
