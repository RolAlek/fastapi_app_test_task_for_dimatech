from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Account(Base):
    balance: Mapped[float] = mapped_column(default=0.0)

    user_oid: Mapped[int] = mapped_column(
        ForeignKey(
            "users.oid",
            ondelete="cascade",
        )
    )
