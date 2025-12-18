from jose import jwt
from app.auth.jwks import get_jwks
from app.core.config import COGNITO_REGION, USER_POOL_ID

ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"


def verify_access_token(token: str) -> dict:
    """
    access_token を検証して payload を返す
    """

    header = jwt.get_unverified_header(token)
    kid = header.get("kid")

    jwks = get_jwks()
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

    # kid 不一致 → JWKS 再取得
    if not key:
        jwks = get_jwks(force_refresh=True)
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

    if not key:
        raise Exception("Invalid kid")

    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        issuer=ISSUER,
        options={"verify_aud": True},
    )

    if payload.get("token_use") != "access":
        raise Exception("Not access token")

    return payload
