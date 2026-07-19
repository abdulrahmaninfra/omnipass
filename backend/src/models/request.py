from pydantic import BaseModel, Field

from ..core.config import get_settings


_settings = get_settings()


class PasswordRequest(BaseModel):
    length: int = Field(
        _settings.DEFAULT_PASSWORD_LENGTH,
        ge=_settings.MIN_PASSWORD_LENGTH,
        le=_settings.MAX_PASSWORD_LENGTH,
    )
    includeArabic: bool = False
