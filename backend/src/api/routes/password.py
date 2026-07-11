from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse

from ...core.generation import PasswordGenerator
from ...models.response import PasswordResponse

router = APIRouter(tags=["Password"])


@router.get("/generate", response_model=PasswordResponse)
def getPassword(
    request: Request,
    length: int = Query(16, ge=8, le=256, description="Password Length"),
    include_arabic: bool = Query(False, description="Include Arabic Characters"),
):

    if not request.query_params:
        return RedirectResponse(url="/generate?length=16&include_arabic=False")
    try:
        generator = PasswordGenerator(length, include_arabic)
        password = generator.generate()

        return PasswordResponse(
            password=password, length=length, includes_arabic=include_arabic
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(500, detail="Internal server error")
