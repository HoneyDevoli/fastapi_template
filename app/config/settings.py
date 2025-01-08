from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(Enum):
    dev: str = 'dev'
    prod: str = 'prod'


class DatabaseSettings(BaseSettings):
    name: str = 'fastapi_db'
    user: str = 'postgres'
    password: str = 'postgres'
    host: str = '0.0.0.0'
    port: int = 5432
    echo: bool = False
    echo_pool: bool = False

    @property
    def url(self) -> str:
        return f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class GlobalSettings(BaseSettings):
    app_name: str
    environment: Environment
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    global_: GlobalSettings = Field(alias='global')
    db: DatabaseSettings = Field(alias='database')

    @property
    def is_dev(self) -> bool:
        return self.global_.environment == Environment.dev


settings: Settings = Settings()
