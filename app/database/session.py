from sqlalchemy.orm import sessionmaker
from app.database.connection import engine

sessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

def getDB():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()
