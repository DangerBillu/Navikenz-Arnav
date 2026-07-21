import json
from typing import Annotated
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from backend.config import settings
from backend.crud import chat_crud, user_crud
from backend.database.connection import get_db
from backend.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized(message: str = "Invalid or expired access token"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _create_guest_user(db: Session, anonymous_user_id: str | None) -> User:
    if not anonymous_user_id:
        anonymous_user_id = "guest"

    user = user_crud.get_or_create_guest_user(db, anonymous_user_id)
    return user


def _transfer_guest_session(db: Session, user: User, anonymous_user_id: str | None) -> User:
    if not anonymous_user_id:
        return user

    guest_user = user_crud.get_guest_user_by_anonymous_id(db, anonymous_user_id)
    if guest_user is None or guest_user.id == user.id:
        return user

    chat_crud.transfer_user_chats(db, guest_user.id, user.id)
    user_crud.delete_user(db, guest_user)
    db.refresh(user)
    return user


def get_token_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict | None:
    if not settings.AUTH0_DOMAIN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auth0 is not configured on the server",
        )
    if credentials is None:
        return None

    try:
        request = Request(
            f"https://{settings.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )
        with urlopen(request, timeout=5) as response:
            return json.load(response)
    except HTTPError:
        return None
    except URLError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not verify the Auth0 token",
        ) from error


def get_current_user(
    claims: dict | None = Depends(get_token_claims),
    db: Session = Depends(get_db),
    anonymous_user_id: Annotated[str | None, Header(alias="X-Anonymous-User-Id")] = None,
):
    if claims is not None:
        subject = claims.get("sub")
        if not subject:
            _unauthorized()
        user = user_crud.get_or_create_auth0_user(db, subject, claims)
        return _transfer_guest_session(db, user, anonymous_user_id)

    if anonymous_user_id:
        return _create_guest_user(db, anonymous_user_id)

    _unauthorized("A bearer token or anonymous user id is required")
