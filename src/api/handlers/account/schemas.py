from datetime import datetime

from src.api.schemas import BaseSchema


class AccountResponseSchema(BaseSchema):
    oid: int
    balance: float
    created_at: datetime
