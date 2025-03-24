from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.services.authentication.service import AuthenticationService

PROVIDERS: Providers = [Scoped(AuthenticationService)]
