import os
import requests
from fastapi import FastAPI, Depends, Response, Cookie, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database.api.api_v1.endpoints import users as users_router
from app.auth.auth import get_current_user
from app.database.db.session import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 起動時にテーブルを作成し DB に接続する準備を行う
@app.on_event("startup")
async def on_startup():
    print("Starting up — init DB (create tables if not exist)")
    await init_db()


COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# ルーター登録
app.include_router(users_router.router, prefix="/api", tags=["users"])


class AuthCode(BaseModel):
    code: str


@app.post("/auth/callback")
def auth_callback(body: AuthCode, response: Response):
    """
    Cognito から authorization_code を access_token / refresh_token に交換する
    """

    token_url = f"{COGNITO_DOMAIN}/oauth2/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": body.code,
        "redirect_uri": REDIRECT_URI,
    }

    token_res = requests.post(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if token_res.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=token_res.json()
        )

    token_json = token_res.json()

    refresh_token = token_json.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh_token")

    # refresh_token は httpOnly Cookie に保存
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # 本番は True（HTTPS）
        samesite="lax",
        path="/auth/refresh"
    )

    # refresh_token は返さない
    return {
        "access_token": token_json["access_token"],
        "id_token": token_json["id_token"],
        "expires_in": token_json["expires_in"],
        "token_type": token_json["token_type"],
    }


@app.post("/auth/refresh")
def auth_refresh(
        response: Response,
        refresh_token: str | None = Cookie(default=None)
):
    """
    httpOnly Cookie の refresh_token を使って access_token を更新する
    """

    print(f"refresh_token: {refresh_token}")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    token_url = f"{COGNITO_DOMAIN}/oauth2/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }

    token_res = requests.post(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if token_res.status_code != 200:
        raise HTTPException(
            status_code=401,
            detail=token_res.json()
        )

    token_json = token_res.json()

    # 🔄 refresh_token ローテーション（返ってきた場合のみ更新）
    new_refresh_token = token_json.get("refresh_token")
    if new_refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth/refresh"
        )

    return {
        "access_token": token_json["access_token"],
        "expires_in": token_json["expires_in"],
        "token_type": token_json["token_type"],
    }


@app.get("/secure")
def secure_api(user=Depends(get_current_user)):
    return {
        "message": "認証成功 🎉",
        "user": user["username"] if "username" in user else user["sub"],
    }
