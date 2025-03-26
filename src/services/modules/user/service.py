from dataclasses import dataclass

from result import Err, Ok

from src.api.handlers.authentication.schemas import UserLoginRequestSchema
from src.api.handlers.user.schemas import (CreateUserRequestSchema,
                                           UpdateUserRequestSchema)
from src.infrastructure.database.models import Token, User
from src.repositories.user import _UserRepository
from src.services.modules.authentication.service import _AuthenticationService
from src.services.modules.user.dto import UserCreateDTO, UserUpdateDTO
from src.services.modules.user.exceptions import (
    PermissionDeniedException, UserNotFoundException,
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
        user: User | None = await self.user_repository.get_user_witch_accounts(user_id)

        if user is None:
            return Err(UserNotFoundException())

        return Ok(user)

    async def get_all_users(self) -> Ok[list[User]]:
        users = await self.user_repository.get_user_witch_accounts()

        return Ok(users)

    async def update_user(self, user_id: int, data: UpdateUserRequestSchema):
        user = await self.user_repository.get_by_pk(user_id)

        if user is None:
            return Err(UserNotFoundException())

        if data.password is not None:
            data.password = self.auth_service.get_pwd_hash(password=data.password)

        dto = UserUpdateDTO(
            email=data.email,
            hashed_password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            is_admin=data.is_admin,
        )

        updated_user = await self.user_repository.update(user, dto)

        return Ok(updated_user)

    async def delete_user(self, user_id: int):
        user = await self.user_repository.get_by_pk(user_id)

        if user is None:
            return Err(UserNotFoundException())

        await self.user_repository.delete(user)

        return Ok(user_id)
