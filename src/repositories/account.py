from dataclasses import dataclass

from src.infrastructure.database.models import Account
from src.repositories.base import BaseSQLAlchemyRepository
from src.services.modules.account.dto import CreateAccountDTO


@dataclass
class _AccountRepository(BaseSQLAlchemyRepository[Account, CreateAccountDTO]):
    model = Account
