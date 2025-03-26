from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.repositories.account import _AccountRepository
from src.services.modules.account.service import AccountService

PROVIDERS: Providers = [Scoped(_AccountRepository), Scoped(AccountService)]
