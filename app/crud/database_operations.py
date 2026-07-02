from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user):
    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        age=user.age
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user