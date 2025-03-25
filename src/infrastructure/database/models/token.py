from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models import User


class Token(Base):
    token: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.oid",
            ondelete="cascade",
        ),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        backref="token",
        lazy="joined",
    )
