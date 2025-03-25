from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.infrastructure.database.models.user import User
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.user.dto import UserCreateDTO


@dataclass
class _UserRepository(BaseSQLAlchemyRepository[User, UserCreateDTO]):
    model = User

    async def get_user_witch_accounts(self, oid: int) -> User | None:
        return await self.session.scalar(
            select(self.model)
            .where(self.model.oid == oid)
            .options(selectinload(self.model.accounts))
        )
