from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import check_database_connection, get_db
from backend.schemas.validation import ForgotPasswordRequest, UserCreate, UserResponse, UserSignIn
from backend.services import services 

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Backend is running",
        "health_url": "/health",
        "docs_url": "/docs",
    }


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


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    created_user = services.CreateUser(db, user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return created_user


@router.post("/signin")
def sign_in(credentials: UserSignIn, db: Session = Depends(get_db)):
    user = services.SignInUser(db, credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {
        "message": "Sign in successful",
        "user": UserResponse.model_validate(user),
    }


@router.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):
    user = services.GetUser(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": f"Welcome back, {user.name}",
        "user": UserResponse.model_validate(user),
    }


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = services.ResetPassword(db, payload.email, payload.new_password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email is not registered")

    return {
        "message": "Password updated successfully",
    }


@router.get("/getusers", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):    
    return services.GetAllUsers(db)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = services.DeleteUser(db, user_id)
    if not deleted:
        return {"message": "User not found"}
    return {"message": "User deleted successfully"}


