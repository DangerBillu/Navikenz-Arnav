import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from backend.config import settings
from backend.crud import user_crud
from backend.database.connection import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized(message: str = "Invalid or expired access token"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_token_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if not settings.AUTH0_DOMAIN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auth0 is not configured on the server",
        )
    if credentials is None:
        _unauthorized("A bearer token is required")

    try:
        request = Request(
            f"https://{settings.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )
        with urlopen(request, timeout=5) as response:
            return json.load(response)
    except HTTPError:
        _unauthorized()
    except URLError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not verify the Auth0 token",
        ) from error


def get_current_user(
    claims: dict = Depends(get_token_claims), db: Session = Depends(get_db)
):
    subject = claims.get("sub")
    if not subject:
        _unauthorized()
    return user_crud.get_or_create_auth0_user(db, subject, claims)
