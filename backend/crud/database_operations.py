from sqlalchemy.orm import Session
from backend.models.user import User

def create_user(db: Session, user, password_hash: str):
    newuser = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        age=user.age,
        password_hash=password_hash,
    )
    
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user_password(db: Session, db_user: User, password_hash: str):
    db_user.password_hash = password_hash
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session):
    return db.query(User).all()

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return db_user
