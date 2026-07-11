from functools import lru_cache
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from sqlalchemy.orm import Session
from backend.config import settings
from backend.crud import user_crud
from backend.database.connection import get_db

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def _jwks_client() -> PyJWKClient:
    return PyJWKClient(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")


def _unauthorized(message: str = "Invalid or expired access token"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_token_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if not settings.AUTH0_DOMAIN or not settings.auth0_audiences:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auth0 is not configured on the server",
        )
    if credentials is None:
        _unauthorized("A bearer token is required")

    try:
        signing_key = _jwks_client().get_signing_key_from_jwt(credentials.credentials)
        return jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.auth0_audiences,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )
    except jwt.PyJWTError:
        _unauthorized()


def get_current_user(
    claims: dict = Depends(get_token_claims), db: Session = Depends(get_db)
):
    subject = claims.get("sub")
    if not subject:
        _unauthorized()
    return user_crud.get_or_create_auth0_user(db, subject, claims)
