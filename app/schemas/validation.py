from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    age: int

class UserResponse(UserCreate):
    id: int
    class Config:
        from_attributes = True
