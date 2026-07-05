import hashlib
import hmac
import secrets

from sqlalchemy.orm import Session
from backend.crud import database_operations as crud
from backend.schemas.validation import UserCreate, UserSignIn

def CreateUser(db: Session, user: UserCreate):
    if crud.get_user_by_email(db, user.email):
        return None

    password_hash = HashPassword(user.password)
    return crud.create_user(db, user, password_hash)

def SignInUser(db: Session, credentials: UserSignIn):
    db_user = crud.get_user_by_email(db, credentials.email)
    if db_user is None or not VerifyPassword(credentials.password, db_user.password_hash):
        return None
    return db_user

def ResetPassword(db: Session, email: str, new_password: str):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        return None

    password_hash = HashPassword(new_password)
    return crud.update_user_password(db, db_user, password_hash)

def DeleteUser(db: Session, user_id: int):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        return None
    return crud.delete_user(db=db, db_user=db_user)

def GetAllUsers(db: Session):
    return crud.get_all_users(db=db)

def GetUser(db: Session, user_id: int):
    return crud.get_user(db=db, user_id=user_id)

def HashPassword(password: str):
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return f"{salt}${password_hash}"

def VerifyPassword(password: str, stored_password: str):
    try:
        salt, saved_hash = stored_password.split("$", 1)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return hmac.compare_digest(password_hash, saved_hash)
