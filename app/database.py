from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

database_url = "postgresql://arnav:pass@localhost:5432/mydatabase"
engine = create_engine(database_url)

# def test_connection():
#     with engine.connect() as connection:
#         return("Connection to postgresql: successful")

def test_connection():
    try:

        with engine.connect() as connection:
            return("Connection to postgresql: successful")
    except SQLAlchemyError as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}