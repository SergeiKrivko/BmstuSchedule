import os
from functools import lru_cache

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


@lru_cache(maxsize=1)
def lks_settings() -> LksSettings:
    return LksSettings()
