from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.repositories.token import _TokenRepository
from src.services.modules.authentication.service import _AuthenticationService

PROVIDERS: Providers = [
    Scoped(_AuthenticationService),
    Scoped(_TokenRepository),
]
