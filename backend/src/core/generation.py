import secrets

from fastapi import HTTPException

from src.core.config import get_settings
from src.core.constants import CharacterSet


class PasswordGenerator:
    def __init__(self, length: int = 16,include_numbers: bool = True,include_alphabit: bool = True,include_punctuation: bool = True,include_arabic: bool = True,include_russian: bool = False,include_abugidas: bool = False,include_katakana: bool = False,include_cherokee: bool = False):        

        settings = get_settings()

        if not (settings.MIN_PASSWORD_LENGTH <= length <= settings.MAX_PASSWORD_LENGTH):
            raise HTTPException(
                400,
                detail=f"Length Must be Between {settings.MIN_PASSWORD_LENGTH}:{settings.MAX_PASSWORD_LENGTH}",
            )

        self.length = length
        self.include_numbers = include_numbers
        self.include_alphabit = include_alphabit
        self.include_punctuation = include_punctuation
        self.include_arabic = include_arabic
        self.include_russian = include_russian
        self.include_abugidas = include_abugidas
        self.include_katakana = include_katakana
        self.include_cherokee = include_cherokee

        self.chars = CharacterSet.get_all()

    def generate(self) -> str:
        password = []
        if self.include_alphabit:
            password.append(secrets.choice(CharacterSet.LOWERCASE))
            password.append(secrets.choice(CharacterSet.UPPERCASE))
        if self.include_numbers:
            password.append(secrets.choice(CharacterSet.DIGITS))
        if self.include_punctuation:
            password.append(secrets.choice(CharacterSet.PUNCTUATION))
        if self.include_russian:
            password.append(secrets.choice(CharacterSet.RUSSIAN))
        if self.include_abugidas:
            password.append(secrets.choice(CharacterSet.ABUGIDAS))
        if self.include_katakana:
            password.append(secrets.choice(CharacterSet.KATAKANA))
        if self.include_cherokee:
            password.append(secrets.choice(CharacterSet.CHEROKEE))
        
        if self.include_arabic:
            password.append(secrets.choice(CharacterSet.ARABIC_LETTERS))
            password.append(secrets.choice(CharacterSet.ARABIC_TASHKEEL))
        remaining = self.length - len(password)
        password.extend(secrets.choice(self.chars) for _ in range(remaining))
        secrets.SystemRandom().shuffle(password)
        return "".join(password)

