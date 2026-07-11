from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import check_database_connection, get_db
from backend.crud import user_crud
from backend.schemas.user import UserProfileSyncRequest, UserResponse
from backend.security import get_current_user, get_token_claims

router = APIRouter(tags=["users"])

@router.get("/health")
def health():
    try:
        check_database_connection()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database is not connected: {error}",
        ) from error

    return {
        "backend": "running",
        "database": "connected",
    }

@router.get("/me", response_model=UserResponse)
def current_user(user=Depends(get_current_user)):
    return user


@router.post("/me", response_model=UserResponse)
def sync_current_user(
    payload: UserProfileSyncRequest,
    claims: dict = Depends(get_token_claims),
    db: Session = Depends(get_db),
):
    subject = claims.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    return user_crud.sync_auth0_user_profile(
        db,
        subject,
        claims,
        payload.model_dump(exclude_none=True),
    )
