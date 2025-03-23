from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from core.settings import AuthSettings


@dataclass
class AuthenticationService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    settings: AuthSettings

    def get_pwd_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.token_expire_minutes
        )
        data.update({"exp": expire})
        return jwt.encode(
            claims=data,
            key=self.settings.secret_key,
            algorithm=self.settings.algorithm,
        )
