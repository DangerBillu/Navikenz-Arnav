from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.validation import ForgotPasswordRequest, UserCreate, UserResponse, UserSignIn
from app.services import services 

router = APIRouter()


@router.get("/createusers")
@router.get("/createusers/", include_in_schema=False)
def create_user_from_browser(
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    age: int | None = None,
    password: str | None = None,
    db: Session = Depends(get_db),
):
    if None in (name, email, phone, age, password):
        return {
            "example": "/createusers?name=Arnav&email=arnav@example.com&phone=1234567890&age=18&password=secret123",
        }

    user = UserCreate(name=name, email=email, phone=phone, age=age, password=password)
    created_user = services.CreateUser(db, user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return created_user


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
    user = services.GetUserByEmail(db, payload.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email is not registered")

    reset_code = services.GenerateForgotPasswordCode()
    return {
        "message": "Password reset code generated",
        "reset_code": reset_code,
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

