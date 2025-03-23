from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Transaction(Base):
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="pos_amount_constr",
        ),
    )

    oid: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[float]

    # realationships
    account_oid: Mapped[int] = mapped_column(
        ForeignKey(
            "accounts.oid",
            ondelete="cascade",
        )
    )
