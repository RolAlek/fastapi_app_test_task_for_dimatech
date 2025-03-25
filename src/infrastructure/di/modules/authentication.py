from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.services.authentication.service import (_AuthenticationService,
                                                 _TokenRepository)

PROVIDERS: Providers = [
    Scoped(_AuthenticationService),
    Scoped(_TokenRepository),
]
