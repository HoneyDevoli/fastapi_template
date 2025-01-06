from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn.config import LOG_LEVELS


class Environment(Enum):
    dev: str = "dev"
    prod: str = "prod"


class DatabaseSettings(BaseSettings):
    name: str = "fastapi_db"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "0.0.0.0"
    port: int = 5432
    echo: bool
    echo_pool: bool

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LogSettings(BaseSettings):
    max_size: int
    max_log_files: int = Field(default=-1)
    log_level: str
    logs_path: str

    @property
    def log_level_upper(self) -> str:
        return self.log_level.upper()

    @field_validator("log_level")
    def valid_loglevel(cls, level: str) -> str:
        if level not in LOG_LEVELS.keys():
            raise ValueError(f"log_level must be one of {LOG_LEVELS.keys()}")
        return level


class GlobalSettings(BaseSettings):
    app_name: str
    environment: Environment
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    global_: GlobalSettings = Field(alias='global')
    db: DatabaseSettings = Field(alias='database')
    log: LogSettings = Field(alias='logging')

    @property
    def is_dev(self) -> bool:
        return self.global_.environment == Environment.dev

settings: Settings = Settings()
