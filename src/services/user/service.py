from dataclasses import dataclass

from result import Err

from src.api.handlers.user.schemas import CreateUserRequestSchema
from src.infrastructure.database.models.user import User
from src.repositories.base import AbstractRepository
from src.services.authentication.service import AuthenticationService
from src.services.user.dto import UserCreateDTO
from src.services.user.exceptions import UserWithEmailAlreadyExistsException


@dataclass
class UserService:
    user_repository: AbstractRepository
    auth_service: AuthenticationService

    async def register_user(
        self,
        data: CreateUserRequestSchema,
    ) -> Err[UserWithEmailAlreadyExistsException] | User:
        if await self.user_repository.get_user_by_email(email=data.email):
            return Err(UserWithEmailAlreadyExistsException())

        dto = UserCreateDTO(
            email=data.email,
            hashed_password=self.auth_service.get_pwd_hash(password=data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )

        user = await self.user_repository.add(data=dto)

        return user
