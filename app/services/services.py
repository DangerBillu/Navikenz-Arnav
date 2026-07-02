from app.crud.database_operations import create_user

def add_user(db, user):
    return create_user(db, user)