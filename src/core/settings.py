from functools import lru_cache
from typing import Type, TypeVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)


@lru_cache
def get_settings(cls: Type[TSettings]) -> TSettings:
    load_dotenv()
    return cls()


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="app_")

    title: str
    host: str
    port: int
    reload: bool


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    driver: str
    host: str
    port: int
    username: str
    password: str
    name: str
    echo: bool

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="jwt_")

    secret_key: str
    algorithm: str
    token_expire_minutes: int


class TransactionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="transaction_")

    secret_key: str
