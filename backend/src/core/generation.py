import secrets

from fastapi import HTTPException

from .config import get_settings
from .constants import CharacterSet


class PasswordGenerator:
    def __init__(self, length: int = 16, include_arabic: bool = False):
        settings = get_settings()

        if not (settings.MIN_PASSWORD_LENGTH <= length <= settings.MAX_PASSWORD_LENGTH):
            raise HTTPException(
                400,
                detail=f"Length Must be Between {settings.MIN_PASSWORD_LENGTH}:{settings.MAX_PASSWORD_LENGTH}",
            )

        self.length = length
        self.include_arabic = include_arabic
        self.chars = CharacterSet.get_all(include_arabic)

    def generate(self) -> str:
        password = [
            secrets.choice(CharacterSet.LOWERCASE),
            secrets.choice(CharacterSet.UPPERCASE),
            secrets.choice(CharacterSet.DIGITS),
            secrets.choice(CharacterSet.PUNCTUATION),
        ]

        if self.include_arabic:
            password.append(secrets.choice(CharacterSet.ARABIC_LETTERS))
            password.append(secrets.choice(CharacterSet.ARABIC_TASHKEEL))

        remaining = self.length - len(password)
        password.extend(secrets.choice(self.chars) for _ in range(remaining))

        secrets.SystemRandom().shuffle(password)
        return "".join(password)
