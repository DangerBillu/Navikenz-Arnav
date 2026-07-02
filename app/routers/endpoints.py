from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.validation import UserCreate, UserResponse
from app.services import services 

router = APIRouter()

@router.post("/createusers", response_model=UserResponse)
@router.post("/createusers/", response_model=UserResponse, include_in_schema=False)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return services.CreateUser(db, user)

@router.get("/createusers")
@router.get("/createusers/", include_in_schema=False)
def create_user_from_browser(
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    age: int | None = None,
    db: Session = Depends(get_db),
):
    if None in (name, email, phone, age):
        return {
            "example": "/createusers?name=Arnav&email=arnav@example.com&phone=1234567890&age=18",
        }

    user = UserCreate(name=name, email=email, phone=phone, age=age)
    return services.CreateUser(db, user)


@router.get("/getusers", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):    
    return services.GetAllUsers(db)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = services.DeleteUser(db, user_id)
    if not deleted:
        return {"message": "User not found"}
    return {"message": "User deleted successfully"}

@router.get("/users/delete/{user_id}", include_in_schema=False)
def delete_user_from_browser(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
