from pydantic import BaseModel


class PasswordResponse(BaseModel):
    password: str
    length: int
    includes_arabic: bool
