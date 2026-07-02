from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

database_url = "postgresql://arnav:pass@localhost:5432/mydatabase"
engine = create_engine(database_url)
