from datetime import datetime

from pydantic import EmailStr, Field

from src.api.schemas import BaseSchema


class UserLoginResponseSchema(BaseSchema):
    token: str
    created_at: datetime


class UserLoginRequestSchema(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=32)
