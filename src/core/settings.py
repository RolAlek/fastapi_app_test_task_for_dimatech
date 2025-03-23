from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    model_config = SettingsConfigDict(env_prefix="app")

    title: str
    host: str
    port: int
    reload: bool


class DatabaseSettings(BaseModel):
    model_config = SettingsConfigDict(env_prefix="database")

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


class AuthSettings(BaseModel):
    model_config = SettingsConfigDict(env_prefix="jwt")

    secret_key: str
    algorithm: str
    token_expire_minutes: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="allow",
    )

    app: AppSettings
    database: DatabaseSettings
