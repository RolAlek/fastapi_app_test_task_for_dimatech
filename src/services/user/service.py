from dataclasses import dataclass

from result import Err, Ok

from src.api.handlers.authentication.schemas import (CreateUserRequestSchema,
                                           UserLoginRequestSchema)
from src.infrastructure.database.models.user import User
from src.repositories.user import _UserRepository
from src.services.authentication.service import _AuthenticationService
from src.services.user.dto import UserCreateDTO
from src.services.user.exceptions import (PermissionDeniedException,
                                          UserWithEmailAlreadyExistsException)


@dataclass
class UserService:
    user_repository: _UserRepository
    auth_service: _AuthenticationService

    async def register_user(
        self,
        data: CreateUserRequestSchema,
    ) -> Err[UserWithEmailAlreadyExistsException] | Ok[User]:
        if await self.user_repository.get_user_by_email(email=data.email):
            return Err(UserWithEmailAlreadyExistsException())

        dto = UserCreateDTO(
            email=data.email,
            hashed_password=self.auth_service.get_pwd_hash(password=data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )

        user = await self.user_repository.add(data=dto)

        return Ok(user)

    async def auth_user(
        self,
        data: UserLoginRequestSchema,
    ) -> Err[PermissionDeniedException] | Ok[str]:
        user = await self.user_repository.get_user_by_email(email=data.email)

        if user is None or not self.auth_service.verify_password(
            data.password, user.hashed_password
        ):
            return Err(PermissionDeniedException())

        access_token = self.auth_service.create_access_token({"sub": user.oid})

        return Ok(access_token)
