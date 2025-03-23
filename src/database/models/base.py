from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    oid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
