from dotenv import load_dotenv
import os, secrets, string, uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

load_dotenv()
MAX_PASSWORD_LENGTH = int(os.getenv("MAX_PASSWORD_LENGTH", "256"))
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))

app = FastAPI(title="OmniPass", description="OmniPass is a Ultimate password generator that compane arabic letter and tashkeel into password")

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],    
)

class CharacterSet:
    lowerCase = list(string.ascii_lowercase)
    upperCase = list(string.ascii_uppercase)
    digits = list(string.digits)
    punctuation = list(string.punctuation)
    arabic_letters = [chr(i) for i in range(0x0621, 0x064B)]
    arabic_tashkeel = [chr(i) for i in range(0x064B, 0x0653)]

class PasswordRequest(BaseModel):
    length: int =  Field(16, ge=MIN_PASSWORD_LENGTH, le=MAX_PASSWORD_LENGTH)
    includeArabic: bool = False

class PasswordResponse(BaseModel):
    password: str
    length: int
    includes_arabic: bool


class PasswordGenerate:
    def __init__(self, length: int = 16, include_arabic: bool = False):
        if not (MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH):
            raise HTTPException(400,detail=f"Length Must be Between {MIN_PASSWORD_LENGTH}:{MAX_PASSWORD_LENGTH}")
        
        chars = (CharacterSet.lowerCase + CharacterSet.upperCase + CharacterSet.digits + CharacterSet.punctuation)
        if include_arabic:
            chars += CharacterSet.arabic_letters + CharacterSet.arabic_tashkeel

        self.length = length
        self.include_arabic = include_arabic
        self.chars = chars

    def generate(self) -> str:
        password = "".join(secrets.choice(self.chars) for _ in range(self.length))
        return password


# generate?length=16&include_arabic=False
@app.get("/generate",response_model=PasswordResponse,tags=["Password"])
def getPassword(request: Request,length: int = Query(16, ge=8, le=256), include_arabic: bool = Query(False)):

    if not request.query_params:
            return RedirectResponse(url="/generate?length=16&include_arabic=False")
    try:
        generator = PasswordGenerate(length, include_arabic)
        password = generator.generate()

        return PasswordResponse(
            password=password,
            length=length,
            includes_arabic= include_arabic)
    
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
    
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")
    
if __name__ == "__main__":
    uvicorn.run("main:app",host=os.getenv("HOST", "0.0.0.0"),port=int(os.getenv("PORT", "8000")))