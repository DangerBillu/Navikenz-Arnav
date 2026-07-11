from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileSyncRequest(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    age: int | None = Field(default=None, ge=0, le=150)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    auth0_subject: str | None
    name: str
    email: str
    phone: str | None
    age: int | None
