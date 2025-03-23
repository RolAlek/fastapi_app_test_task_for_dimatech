from pydantic import BaseModel, EmailStr, Field


class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=32)
    first_name: str = Field(min_length=2, max_length=128)
    last_name: str = Field(min_length=2, max_length=128)
