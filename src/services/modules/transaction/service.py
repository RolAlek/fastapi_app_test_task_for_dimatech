import hashlib
from dataclasses import dataclass

from result import Err, Ok

from src.api.handlers.transaction.schemas import TransactionRequestSchema
from src.core.settings import TransactionSettings
from src.infrastructure.database.models.transaction import Transaction
from src.repositories.transaction import _TransactionRepository
from src.services.modules.account.dto import CreateAccountDTO
from src.services.modules.account.service import AccountService
from src.services.modules.transaction.dto import CreateTransactionDto
from src.services.modules.transaction.exceptions import (
    InvalidSignatureException, TransactionNotUniqueException)
from src.services.modules.user.exceptions import UserNotFoundException
from src.services.modules.user.service import UserService


@dataclass
class TransactionService:
    user_service: UserService
    account_service: AccountService
    transaction_repository: _TransactionRepository
    settings: TransactionSettings

    async def allocate_transaction(
        self,
        data: TransactionRequestSchema,
    ) -> (
        Err[
            InvalidSignatureException
            | TransactionNotUniqueException
            | UserNotFoundException
        ]
        | Ok[Transaction]
    ):
        if not self._check_signature(data):
            return Err(InvalidSignatureException())

        if await self.transaction_repository.check_exists(data.transaction_id):
            return Err(TransactionNotUniqueException())

        user_or_error = await self.user_service.get_user(data.user_id)

        if isinstance(user_or_error, Err):
            return user_or_error

        user = user_or_error.ok_value

        account = next(
            (acc for acc in user.accounts if acc.oid == data.account_id),
            None,
        )

        if account is None:
            dto = CreateAccountDTO(oid=data.account_id, user_oid=user.oid)
            account = await self.account_service.add_account(dto)

        transaction_dto = CreateTransactionDto(
            oid=data.transaction_id,
            amount=data.amount,
            account_oid=account.oid,
        )
        transaction = await self.transaction_repository.add(transaction_dto)
        return Ok(transaction)

    def _check_signature(self, data: TransactionRequestSchema) -> bool:
        signature_string = f"{data.account_id}{data.amount}{data.transaction_id}{data.user_id}{self.settings.secret_key}"
        cltd_signature = hashlib.sha256(signature_string.encode()).hexdigest()

        if cltd_signature != data.signature:
            return False

        return True
