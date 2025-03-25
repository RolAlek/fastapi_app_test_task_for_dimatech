from typing import assert_never

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException, status
from result import Err

from src.api.dependecies import current_superuser, current_user
from src.api.handlers.user.schemas import (CreateUserRequestSchema,
                                           CreateUserResponseSchema,
                                           ReadUserResponseSchema)
from src.infrastructure.database.models.user import User
from src.services.user import exceptions as user_exceptions
from src.services.user.service import UserService

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponseSchema,
)
@inject
async def register_user(
    data: CreateUserRequestSchema,
    service: Injected[UserService],
    user: User = Depends(current_superuser),
):
    user = await service.register(data)

    if isinstance(user, Err):
        match user.err_value:
            case user_exceptions.UserWithEmailAlreadyExistsException():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User with email is already registered. Email: {data.email}.",
                )
            case _ as never:
                assert_never(never)

    return user.ok_value


@router.get("/me", response_model=ReadUserResponseSchema)
@inject
async def get_me(user: User = Depends(current_user)):
    return user
