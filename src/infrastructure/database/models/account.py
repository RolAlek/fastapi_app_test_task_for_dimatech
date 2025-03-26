from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database._types import _updated_at
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.transaction import Transaction


class Account(Base):
    user_oid: Mapped[int] = mapped_column(
        ForeignKey(
            "users.oid",
            ondelete="cascade",
        )
    )
    updated_at: Mapped[_updated_at]

    # relationships
    transactions: Mapped[list["Transaction"]] = relationship(backref="account")

    @hybrid_property
    def balance(self) -> float:
        if self.transactions:
            return float(sum((tx.amount for tx in self.transactions)))
        return float(0)

    @balance.inplace.expression
    @classmethod
    def balance_expression(cls):
        return (
            select(func.sum(Transaction.amount))
            .where(Transaction.account_oid == cls.oid)
            .label("balance")
        )
