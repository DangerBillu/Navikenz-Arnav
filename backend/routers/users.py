from fastapi import APIRouter, HTTPException, status

from backend.database.connection import check_database_connection

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

