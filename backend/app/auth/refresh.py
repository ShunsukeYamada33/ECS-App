from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")


@router.post("/auth/refresh")
def refresh_token(payload: dict):
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")

    res = requests.post(
        f"{COGNITO_DOMAIN}/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "refresh_token": refresh_token,
        },
    )

    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Refresh failed")

    return res.json()
