from fastapi import APIRouter, HTTPException, Request, status
from src.core.generation import PasswordGenerator
from src.models.response import PasswordResponse
from src.models.request import PasswordGenerateRequest
router = APIRouter(tags=["Password"])


@router.post("/generate", response_model=PasswordResponse)
def generate_password(payload: PasswordGenerateRequest):

    try: 
        generation = PasswordGenerator(**payload.model_dump())
        password = generation.generate()

        return PasswordResponse(password = password, **payload.model_dump())

    except (HTTPException, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request parameters",
        )


    

