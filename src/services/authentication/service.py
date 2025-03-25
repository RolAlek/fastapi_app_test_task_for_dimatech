from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from src.core.settings import AuthSettings
from src.infrastructure.database.models.token import Token
from src.repositories.token import _TokenRepository
from src.repositories.user import _UserRepository
from src.services.authentication.dto import CreateTokenDTO


@dataclass
class _AuthenticationService:
    token_repository: _TokenRepository
    user_repository: _UserRepository
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    settings: AuthSettings

    def get_pwd_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, payload: dict[str, str]) -> Token:
        token = await self.token_repository.get_by_attr("user_id", int(payload["sub"]))

        if token:
            return token

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.token_expire_minutes
        )

        payload.update({"exp": expire})

        access_token = await self.token_repository.add(
            CreateTokenDTO(
                token=jwt.encode(
                    claims=payload,
                    key=self.settings.secret_key,
                    algorithm=self.settings.algorithm,
                ),
                user_id=int(payload["sub"]),
            )
        )

        return access_token

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
