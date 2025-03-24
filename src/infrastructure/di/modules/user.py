from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.repositories.base import AbstractRepository
from src.repositories.user import UserRepository
from src.services.user.service import UserService

PROVIDERS: Providers = [
    Scoped(UserRepository, type_=AbstractRepository),
    Scoped(UserService),
]
