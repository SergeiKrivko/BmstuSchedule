import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "local")
ENVS_DIR = "envs"
ENV_FILE = f"{ENVS_DIR}/{ENV}.env"
COMMON_ENV_FILE = f"{ENVS_DIR}/common.env"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(COMMON_ENV_FILE, ENV_FILE),
        env_nested_delimiter="__",
        extra="ignore",
    )


class LksSettings(EnvSettings):
    model_config = SettingsConfigDict(
        env_prefix="LKS__",
    )

    base_api_url: str
    use_ssl: bool


class DbSettings(EnvSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB__",
    )

    name: str
    host: str
    port: int
    user: str
    password: str = Field(alias="db__pass")
    max_connections: int = 5

    @property
    def access_str(self) -> str:
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.access_str}"


@lru_cache(maxsize=1)
def lks_settings() -> LksSettings:
    return LksSettings()


@lru_cache(maxsize=1)
def db_settings() -> DbSettings:
    return DbSettings()
