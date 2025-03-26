import itertools
from functools import lru_cache, partial
from typing import Iterable

import aioinject
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import (AppSettings, AuthSettings, DatabaseSettings,
                               TransactionSettings, get_settings)
from src.infrastructure.database.dependencies import create_session
from src.infrastructure.di.modules import (ACCOUNT_PROVIDERS,
                                           AUTHENTICATION_PROVIDERS,
                                           TRANSACTION_PROVIDERS,
                                           USER_PROVIDERS)

MODULES = [
    ACCOUNT_PROVIDERS,
    AUTHENTICATION_PROVIDERS,
    TRANSACTION_PROVIDERS,
    USER_PROVIDERS,
]

SETTINGS = [AppSettings, AuthSettings, DatabaseSettings, TransactionSettings]


def _init_settings(
    container: aioinject.Container,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        factory = partial(get_settings, settings_cls)
        container.register(aioinject.Singleton(factory, type_=settings_cls))


@lru_cache
def init_container() -> aioinject.Container:
    container = aioinject.Container()
    container.register(aioinject.Scoped(create_session, type_=AsyncSession))

    for provider in itertools.chain.from_iterable(MODULES):
        container.register(provider)

    _init_settings(container, SETTINGS)

    return container
