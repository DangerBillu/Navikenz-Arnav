from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    auth0_subject = Column(String(255), unique=True, index=True, nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)
    password_hash = Column(String(255), nullable=True)

    chats = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
