import time
import requests
from typing import Dict, Any
from app.core.config import COGNITO_REGION, USER_POOL_ID

ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

_JWKS_CACHE: Dict[str, Any] | None = None
_JWKS_EXPIRES_AT: float = 0

JWKS_TTL_SECONDS = 60 * 60 * 24  # 24時間


def _fetch_jwks() -> Dict[str, Any]:
    res = requests.get(JWKS_URL, timeout=5)
    res.raise_for_status()
    return res.json()


def get_jwks(force_refresh: bool = False) -> Dict[str, Any]:
    """
    JWKS をキャッシュ付きで取得する
    """
    global _JWKS_CACHE, _JWKS_EXPIRES_AT

    now = time.time()

    if not force_refresh and _JWKS_CACHE and now < _JWKS_EXPIRES_AT:
        return _JWKS_CACHE

    try:
        jwks = _fetch_jwks()
        _JWKS_CACHE = jwks
        _JWKS_EXPIRES_AT = now + JWKS_TTL_SECONDS
        return jwks
    except Exception:
        # 取得失敗時でも古いキャッシュがあれば使う
        if _JWKS_CACHE:
            return _JWKS_CACHE
        raise
