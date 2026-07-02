from pydentic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(UserCreate):
    id: int
    class Config:
        from_attributes = True