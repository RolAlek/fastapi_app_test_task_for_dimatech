from typing import assert_never

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException, status
from result import Err

from src.api.dependencies import current_superuser, current_user
from src.api.handlers.user.schemas import (CreateUserRequestSchema,
                                           CreateUserResponseSchema,
                                           ReadUserForAdminResponseSchema,
                                           ReadUserResponseSchema,
                                           UpdateUserRequestSchema)
from src.infrastructure.database.models.user import User
from src.services.modules.user import exceptions as user_exceptions
from src.services.modules.user.service import UserService

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
    user = await service.register_user(data)

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


@router.get("/", response_model=list[ReadUserForAdminResponseSchema])
@inject
async def get_all_users(
    service: Injected[UserService],
    user: User = Depends(current_superuser),
):
    users = await service.get_all_users()

    return users.ok_value


@router.get("/me", response_model=ReadUserResponseSchema)
@inject
async def get_me(service: Injected[UserService], user: User = Depends(current_user)):
    user_with_accs = await service.get_user(user.oid)
    return user_with_accs.ok_value


@router.get("/{user_id}", response_model=ReadUserForAdminResponseSchema)
@inject
async def get_user(
    user_id: int,
    service: Injected[UserService],
    user: User = Depends(current_superuser),
):
    user = await service.get_user(user_id)

    if isinstance(user, Err):
        match user.err_value:
            case user_exceptions.UserNotFoundException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with '{user_id}' not found.",
                )
            case _ as never:
                assert_never(never)

    return user.ok_value


@router.patch("/{user_id}", response_model=ReadUserForAdminResponseSchema)
@inject
async def update_user(
    user_id: int,
    data: UpdateUserRequestSchema,
    service: Injected[UserService],
    user: User = Depends(current_superuser),
):
    updated_user = await service.update_user(user_id, data)

    if isinstance(updated_user, Err):
        match updated_user.err_value:
            case user_exceptions.UserNotFoundException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with '{user_id}' not found.",
                )
            case _ as never:
                assert_never(never)

    return updated_user.ok_value


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: int,
    service: Injected[UserService],
    user: User = Depends(current_superuser),
):
    result = await service.delete_user(user_id)

    if isinstance(result, Err):
        match result.err_value:
            case user_exceptions.UserNotFoundException():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with '{user_id}' not found.",
                )
            case _ as never:
                assert_never(never)
