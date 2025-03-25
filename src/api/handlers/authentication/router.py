from typing import assert_never

from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException, Response, status
from result import Err

from src.api.handlers.authentication.schemas import (CreateUserRequestSchema,
                                           CreateUserResponseSchema,
                                           UserLoginRequestSchema,
                                           UserLoginResponseSchema)
from src.services.user import exceptions as user_exceptions
from src.services.user.service import UserService

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponseSchema,
)
@inject
async def register_user(
    data: CreateUserRequestSchema,
    service: Injected[UserService],
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


@router.post(
    "/login",
    response_model=UserLoginResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def login(
    data: UserLoginRequestSchema,
    response: Response,
    user_service: Injected[UserService],
):
    token = await user_service.auth_user(data)

    if isinstance(token, Err):
        match token.err_value:
            case user_exceptions.PermissionDeniedException():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User with email or password is not registered.",
                )
            case _ as never:
                assert_never(never)

    response.set_cookie(key="access_token", value=token.ok_value, httponly=True)

    return UserLoginResponseSchema(access_token=token.ok_value)
