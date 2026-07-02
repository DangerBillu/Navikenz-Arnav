from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user):
    newuser = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        age=user.age
    )
    
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return db_user
