from dataclasses import dataclass

from src.infrastructure.database.models.token import Token
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.authentication.dto import CreateTokenDTO


@dataclass
class _TokenRepository(BaseSQLAlchemyRepository[Token, CreateTokenDTO]):
    model = Token
