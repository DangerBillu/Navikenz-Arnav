from sqlalchemy.orm import DeclarativeBase, Integer, String, Column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(int(10))
    age = Column(Integer)
