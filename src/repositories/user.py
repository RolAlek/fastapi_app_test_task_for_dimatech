from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.infrastructure.database.models.user import User
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.user.dto import UserCreateDTO


@dataclass
class _UserRepository(BaseSQLAlchemyRepository[User, UserCreateDTO]):
    model = User

    async def get_user_witch_accounts(
        self,
        oid: int | None = None,
    ) -> User | list[User] | None:
        stmt = select(self.model).options(selectinload(self.model.accounts))

        if oid:
            stmt = stmt.where(self.model.oid == oid)
            return await self.session.scalar(stmt)

        return (await self.session.scalars(stmt)).all()
