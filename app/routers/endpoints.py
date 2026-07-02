from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.validation import UserCreate
from app.services import services 

app = APIRouter()

@app.post("/createusers")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return services.CreateUser(db, user)


@app.get("/getusers")
def get_users(db: Session = Depends(get_db)):    
    return services.GetAllUsers(db)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    services.DeleteUser(db, user_id)
    return {"message": "User deleted successfully"}
