import os

from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests

router = APIRouter()
COGNITO_REGION = os.getenv("COGNITO_REGION")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

jwks = requests.get(JWKS_URL).json()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_jwt(token: str):
    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=APP_CLIENT_ID,
            issuer=ISSUER,
            options={
                "verify_aud": False,  # ← aud を検証しない
            },
        )
        print(payload)

        # token_use を必ずチェック
        if payload.get("token_use") != "access":
            raise Exception("Not an access token")

        return payload  # ← 検証済みユーザー情報

    except Exception:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload
