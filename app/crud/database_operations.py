from sqlalchemy.orm import Session
from app.models.user import User

def createUser(db: Session, user):
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

def deleteUser(db: Session, dbuser: User):
    db.delete(dbuser)
    db.commit()
    return dbuser