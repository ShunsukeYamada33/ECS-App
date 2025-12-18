import requests
from fastapi import HTTPException

from app.core.config import COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI
import app.core.constants.cookies as cookies


def exchange_code_for_token(code: str) -> dict:
    """
    認証コード → トークン 交換
    """
    token_url = f"{COGNITO_DOMAIN}/oauth2/token"

    data = {
        "grant_type": cookies.AUTHORIZATION,
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    res = requests.post(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if res.status_code != 200:
        raise HTTPException(status_code=400, detail=res.json())

    return res.json()


def refresh_access_token(refresh_token: str) -> dict:
    """
    refresh_token → access_token 更新
    """
    token_url = f"{COGNITO_DOMAIN}/oauth2/token"

    data = {
        "grant_type": cookies.REFRESH,
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }

    res = requests.post(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if res.status_code != 200:
        raise HTTPException(status_code=401, detail=res.json())

    return res.json()
