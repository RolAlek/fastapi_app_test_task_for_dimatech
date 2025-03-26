from aioinject import Scoped

from src.infrastructure.di._types import Providers
from src.repositories.transaction import _TransactionRepository
from src.services.transaction.service import TransactionService

PROVIDERS: Providers[
    Scoped(_TransactionRepository),
    Scoped(TransactionService),
]
