from dataclasses import dataclass

from sqlalchemy import select

from database.models.user import User
from repositories.base import BaseSQLAlchemyRepository


@dataclass
class UserRepository(BaseSQLAlchemyRepository):
    model = User

    async def get_user_by_email(self, email: str) -> User:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
