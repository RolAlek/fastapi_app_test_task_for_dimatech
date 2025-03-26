from typing import assert_never

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException, status
from result import Err

from src.api.dependencies import current_user
from src.api.handlers.transaction.schemas import (AccountResponseSchema,
                                                  TransactionRequestSchema)
from src.infrastructure.database.models.user import User
from src.services.modules.account.service import AccountService
from src.services.modules.transaction import \
    exceptions as transaction_exceptions
from src.services.modules.transaction.service import TransactionService
from src.services.modules.user import exceptions as user_exceptions

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def accept_transaction(
    data: TransactionRequestSchema,
    service: Injected[TransactionService],
):
    transaction = await service.allocate_transaction(data)

    if isinstance(transaction, Err):
        match transaction.err_value:
            case user_exceptions.UserNotFoundException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with `{data.user_id}` not registered.",
                )
            case transaction_exceptions.TransactionNotUniqueException():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Transaction with `{data.transaction_id}` already exist.",
                )
            case transaction_exceptions.InvalidSignatureException():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid `{data.signature}` signature",
                )
            case _ as never:
                assert_never(never)


@router.get("/accounts/me", response_model=list[AccountResponseSchema])
@inject
async def get_my_accounts(
    service: Injected[AccountService],
    user: User = Depends(current_user),
):
    return await service.get_all_accounts_for_user(user.oid)
