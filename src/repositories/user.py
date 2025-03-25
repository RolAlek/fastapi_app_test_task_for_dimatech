from dataclasses import dataclass

from src.infrastructure.database.models.user import User
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.user.dto import UserCreateDTO


@dataclass
class _UserRepository(BaseSQLAlchemyRepository[User, UserCreateDTO]):
    model = User
