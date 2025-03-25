from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.services.authentication.service import _AuthenticationService

PROVIDERS: Providers = [Scoped(_AuthenticationService)]
