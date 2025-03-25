from dataclasses import dataclass

from result import Err, Ok

from src.api.handlers.authentication.schemas import UserLoginRequestSchema
from src.api.handlers.user.schemas import CreateUserRequestSchema
from src.infrastructure.database.models import Token, User
from src.repositories.user import _UserRepository
from src.services.authentication.service import _AuthenticationService
from src.services.user.dto import UserCreateDTO
from src.services.user.exceptions import (PermissionDeniedException,
                                          UserNotFoundException,
                                          UserWithEmailAlreadyExistsException)


@dataclass
class UserService:
    user_repository: _UserRepository
    auth_service: _AuthenticationService

    async def register_user(
        self,
        data: CreateUserRequestSchema,
    ) -> Err[UserWithEmailAlreadyExistsException] | Ok[User]:
        if await self.user_repository.get_by_attr("email", data.email):
            return Err(UserWithEmailAlreadyExistsException())

        dto = UserCreateDTO(
            email=data.email,
            hashed_password=self.auth_service.get_pwd_hash(password=data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )

        user = await self.user_repository.add(data=dto)

        return Ok(user)

    async def auth(
        self,
        data: UserLoginRequestSchema,
    ) -> Err[PermissionDeniedException] | Ok[Token]:
        user = await self.user_repository.get_by_attr("email", data.email)

        if user is None or not self.auth_service.verify_password(
            data.password, user.hashed_password
        ):
            return Err(PermissionDeniedException())

        access_token = await self.auth_service.create_access_token(
            {"sub": str(user.oid)}
        )

        return Ok(access_token)

    async def get_user(
        self,
        user_id: int,
    ) -> Err[UserNotFoundException] | Ok[User]:
        user = await self.user_repository.get_user_witch_accounts(user_id)

        if user is None:
            return Err(UserNotFoundException())

        return Ok(user)

    async def get_all_users(self) -> Ok[list[User]]:
        users = await self.user_repository.get_user_witch_accounts()

        return Ok(users)
