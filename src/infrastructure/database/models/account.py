from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database._types import _updated_at
from src.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models import Transaction


class Account(Base):
    balance: Mapped[float] = mapped_column(default=0.0)

    user_oid: Mapped[int] = mapped_column(
        ForeignKey(
            "users.oid",
            ondelete="cascade",
        )
    )
    updated_at: Mapped[_updated_at]

    # relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        backref="account",
        cascade="delete",
    )
