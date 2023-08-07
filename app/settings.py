from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Extra

from utils.schemas.database import DatabaseSettingsMixin


class Settings(BaseSettings, DatabaseSettingsMixin):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ENVIRONMENT: Optional[str]

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "lhgGHo7t8O7Ff68OF688o68O6F6fF68O"
    JWT_ALGORITHM = "HS256"

    ALLOWED_HOSTS: list = []

    TIME_ZONE = "UTC"

    class Config:
        """Configuration class that allows to overwrite the behavior of the BaseSettings."""

        case_sensitive: bool = False
        extra = Extra.ignore
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()
