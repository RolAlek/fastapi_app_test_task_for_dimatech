from typing import TYPE_CHECKING

from sqlalchemy import Computed, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base

if TYPE_CHECKING:
    from src.database.models import Account


class User(Base):
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(
        String(257),
        Computed("first_name || ' ' || last_name", persisted=True),
    )
    is_admin: Mapped[bool] = mapped_column(default=False)

    # relationships
    accounts: Mapped[list["Account"]] = relationship(
        backref="user",
        lazy="selectin",
        cascade="delete",
    )
