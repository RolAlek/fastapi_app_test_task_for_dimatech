from dataclasses import dataclass
from typing import Sequence

from src.infrastructure.database.models.account import Account
from src.repositories.account import _AccountRepository
from src.services.modules.account.dto import CreateAccountDTO


@dataclass
class AccountService:
    account_repository: _AccountRepository

    async def add_account(self, dto: CreateAccountDTO) -> Account:
        return await self.account_repository.add(dto)

    async def get_all_accounts_for_user(self, user_oid: int) -> Sequence[Account]:
        return await self.account_repository.get_list(user_oid=user_oid)
