from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.validation import UserCreate
from app.services.user_service import add_user

router = APIRouter()

@router.post("/users")
def create(user: UserCreate, db: Session = Depends(get_db)):
    return add_user(db, user)