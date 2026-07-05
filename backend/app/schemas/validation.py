from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    age: int
    password: str = Field(min_length=6)

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    age: int

    class Config:
        from_attributes = True
