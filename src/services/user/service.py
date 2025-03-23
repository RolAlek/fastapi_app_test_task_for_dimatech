from dataclasses import dataclass

from result import Err

from api.handlers.user.shcemas import CreateUserRequestSchema
from repositories.user import UserRepository
from services.base import AbstractService
from services.user.dto import UserCreateDTO
from services.user.exceptions import UserWithEmailAlreadyExistsException
from src.services.authentication.service import AuthenticationService


@dataclass
class UserService(AbstractService):
    repository: UserRepository = UserRepository()
    auth_service = AuthenticationService()

    async def register_user(self, data: CreateUserRequestSchema):
        if await self.repository.get_user_by_email(email=data.email):
            Err(UserWithEmailAlreadyExistsException())

        dto = UserCreateDTO(
            email=data.email,
            hashed_password=self.auth_service.get_pwd_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )

        user = await self.repository.add(dto)

        return user
