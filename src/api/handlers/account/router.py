from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends

from src.api.dependencies import current_user
from src.api.handlers.account.schemas import AccountResponseSchema
from src.infrastructure.database.models.user import User
from src.services.modules.account.service import AccountService

router = APIRouter()


@router.get("/me", response_model=list[AccountResponseSchema])
@inject
async def get_my_accounts(
    service: Injected[AccountService],
    user: User = Depends(current_user),
):
    return await service.get_user_accounts(user.oid)
