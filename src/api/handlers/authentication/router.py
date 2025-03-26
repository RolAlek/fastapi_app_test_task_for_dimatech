from typing import assert_never

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException, status
from result import Err

from src.api.handlers.authentication.schemas import (UserLoginRequestSchema,
                                                     UserLoginResponseSchema)
from src.services.modules.user import exceptions as user_exceptions
from src.services.modules.user.service import UserService

router = APIRouter()


@router.post(
    "/login",
    response_model=UserLoginResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def login(
    data: UserLoginRequestSchema,
    user_service: Injected[UserService],
):
    token = await user_service.auth(data)

    if isinstance(token, Err):
        match token.err_value:
            case user_exceptions.PermissionDeniedException():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User with email or password is not registered.",
                )
            case _ as never:
                assert_never(never)

    return token.ok_value
