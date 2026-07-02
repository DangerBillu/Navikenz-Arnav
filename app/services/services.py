from sqlalchemy.orm import Session
from app.crud import database_operations as crud
from app.schemas.validation import UserCreate

def CreateUser(db:Session, user: UserCreate):
    return crud.create_user(db, user)

def DeleteUser(db:Session, user_id: int):
    db_user = crud.getUser(db, user_id)
    if db_user is None:
        return ("user not found error")
    return crud.delete_user(db=db, db_user=db_user)

def GetAllUsers(db: Session):
    return crud.get_all_users(db=db)