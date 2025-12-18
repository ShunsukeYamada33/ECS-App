from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/secure")
def secure_api(user=Depends(get_current_user)):
    return {
        "message": "認証成功 🎉",
        "user": user["username"] if "username" in user else user["sub"],
    }
