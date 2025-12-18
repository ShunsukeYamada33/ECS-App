from fastapi import APIRouter, Response, Cookie, HTTPException, Header
from pydantic import BaseModel

import app.auth.service as auth_service
import app.core.constants.cookies as cookies
import app.core.constants.headers as headers
from app.auth.csrf import generate_csrf_token

router = APIRouter()


class AuthCode(BaseModel):
    code: str


@router.post("/callback")
def auth_callback(body: AuthCode, response: Response):
    token_json = auth_service.exchange_code_for_token(body.code)

    refresh_token = token_json.get(cookies.REFRESH)
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh_token")

    refresh_token = token_json.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh_token")

    csrf_token = generate_csrf_token()

    # refresh_token は httpOnly Cookie
    response.set_cookie(
        key=cookies.REFRESH,
        value=refresh_token,
        httponly=True,
        secure=False,  # 本番 True
        samesite="lax",
        path="/auth/refresh",
    )

    response.set_cookie(
        key=cookies.CSRF,
        value=csrf_token,
        httponly=False,
        secure=False,
        samesite="lax",
        path="/",
    )

    return {
        "access_token": token_json[cookies.ACCESS],
        "id_token": token_json[cookies.ID_TOKEN],
        "expires_in": token_json[cookies.EXPIRES_IN],
        "token_type": token_json[cookies.TOKEN_TYPE],
    }


@router.post("/refresh")
def auth_refresh(
        response: Response,
        refresh_token: str | None = Cookie(default=None, alias=cookies.REFRESH),
        csrf_token: str | None = Cookie(default=None, alias=cookies.CSRF),
        csrf_header: str | None = Header(default=None, alias=headers.CSRF),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    # CSRF 検証
    if not csrf_token or not csrf_header or csrf_token != csrf_header:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    token_json = auth_service.refresh_access_token(refresh_token)

    # refresh_token ローテーション対応
    new_refresh_token = token_json.get(cookies.REFRESH)
    if new_refresh_token:
        response.set_cookie(
            key=cookies.REFRESH,
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth/refresh",
        )

    return {
        "access_token": token_json[cookies.ACCESS],
        "expires_in": token_json[cookies.EXPIRES_IN],
        "token_type": token_json[cookies.TOKEN_TYPE],
    }
