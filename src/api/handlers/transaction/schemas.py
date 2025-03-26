from src.api.schemas import BaseSchema


class TransactionRequestSchema(BaseSchema):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str
