from pathlib import Path, PosixPath
from typing import Optional

from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.database.schemas import DatabaseSettingsMixin


class Settings(BaseSettings, DatabaseSettingsMixin):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR: PosixPath = Path(__file__).resolve().parent.parent

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG: bool = False
    # ENVIRONMENT: Optional[str]

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY: str = "lhgGHo7t8O7Ff68OF688o68O6F6fF68O"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    ALLOWED_HOSTS: list = []

    TIME_ZONE: str = "UTC"

    model_config = SettingsConfigDict(
        # Configuration for BaseSettings.
        case_sensitive=False,
        extra=Extra.ignore,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
