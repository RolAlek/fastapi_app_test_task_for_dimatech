from datetime import datetime
from typing import Optional, Self

from pydantic import EmailStr, Field, model_validator

from src.api.schemas import BaseSchema


class AccountSchema(BaseSchema):
    oid: int
    balance: float
    created_at: datetime
    updated_at: datetime


class CreateUserRequestSchema(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=32)
    password_repeat: str = Field(..., min_length=6, max_length=32)
    first_name: str = Field(..., min_length=2, max_length=128)
    last_name: str = Field(..., min_length=2, max_length=128)

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")

        if self.email in self.password:
            raise ValueError("Password should not contain email")

        return self


class CreateUserResponseSchema(BaseSchema):
    oid: int
    email: EmailStr
    full_name: str
    is_admin: bool
    created_at: datetime
    accounts: list = Field(default_factory=list)


class ReadUserResponseSchema(BaseSchema):
    oid: int
    email: EmailStr
    full_name: str


class ReadUserForAdminResponseSchema(BaseSchema):
    oid: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    accounts: list[AccountSchema] = Field(default_factory=list)


class UpdateUserRequestSchema(BaseSchema):
    email: Optional[EmailStr]
    password: str = Field(None, min_length=6, max_length=32)
    first_name: Optional[str] = Field(None, min_length=2, max_length=128)
    last_name: Optional[str] = Field(None, min_length=2, max_length=128)
    is_admin: Optional[bool] = None
