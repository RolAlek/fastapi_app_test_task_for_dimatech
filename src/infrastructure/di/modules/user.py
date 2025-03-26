from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.repositories.user import _UserRepository
from src.services.modules.user.service import UserService

PROVIDERS: Providers = [
    Scoped(_UserRepository),
    Scoped(UserService),
]
