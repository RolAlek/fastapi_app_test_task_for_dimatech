from dataclasses import dataclass


@dataclass
class UserCreateDTO:
    email: str
    hashed_password: str
    first_name: str
    last_name: str
