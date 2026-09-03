from pydantic import BaseModel


class PasswordResponse(BaseModel):
    password: str
    length: int
    include_numbers: bool
    include_alphabit: bool
    include_punctuation: bool
    include_arabic: bool
    include_russian: bool
    include_abugidas: bool
    include_katakana: bool
    include_cherokee: bool