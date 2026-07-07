from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.schemas.user import ForgotPasswordRequest, UserCreate, UserResponse, UserSignIn
from backend.services import user_services 

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    created_user = user_services.CreateUser(db, user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return created_user

@router.post("/signin")
def sign_in(credentials: UserSignIn, db: Session = Depends(get_db)):
    user = user_services.SignInUser(db, credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {
        "message": "Sign in successful",
        "user": UserResponse.model_validate(user),
    }

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_services.ResetPassword(db, payload.email, payload.new_password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email is not registered")

    return {
        "message": "Password updated successfully",
    }




