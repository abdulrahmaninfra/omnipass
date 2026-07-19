from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    API_TITLE: str = "OmniPass"
    API_DESCRIPTION: str = (
        "A password generator with Arabic letter and tashkeel support"
    )

    API_VERSION: str = "1.1.0"

    ALLOWED_ORIGINS: list[str] = ["https://omnipass-mu.vercel.app/"]
    ALLOWED_METHODS: list[str] = ["GET"]
    MIN_PASSWORD_LENGTH: int = 8
    MAX_PASSWORD_LENGTH: int = 256
    DEFAULT_PASSWORD_LENGTH: int = 16

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
