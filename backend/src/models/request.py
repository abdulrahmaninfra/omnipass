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

class PasswordGenerateRequest(BaseModel):
    length: int = Field(default=16, ge=8, le=256, description="Password length")
    include_numbers: bool = Field(default=True, description="Include digits (0-9)")
    include_alphabit: bool = Field(default=True, description="Include Latin letters (a-z, A-Z)")
    include_punctuation: bool = Field(default=True, description="Include punctuation and symbols")
    include_arabic: bool = Field(default=False, description="Include Arabic letters and Tashkeel")
    include_russian: bool = Field(default=False, description="Include Russian / Cyrillic letters")
    include_abugidas: bool = Field(default=False, description="Include Abugidas (Devanagari)")
    include_katakana: bool = Field(default=False, description="Include Japanese Katakana")
    include_cherokee: bool = Field(default=False, description="Include Cherokee Syllabary")