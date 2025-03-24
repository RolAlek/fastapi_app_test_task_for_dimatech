from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException, status
from result import Err

from src.api.handlers.user.schemas import (CreateUserRequestSchema,
                                           CreateUserResponseSchema)
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

    return user
