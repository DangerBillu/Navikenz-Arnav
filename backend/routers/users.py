from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import check_database_connection, get_db
from backend.schemas.user import UserResponse
from backend.services import user_services
from backend.services import chat_services

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

@router.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):
    user = user_services.GetUser(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    stats = chat_services.GetDashboardStats(db, user_id)

    return {
        "message": f"Welcome back, {user.name}",
        "user": UserResponse.model_validate(user),
        "stats": stats,
    }

