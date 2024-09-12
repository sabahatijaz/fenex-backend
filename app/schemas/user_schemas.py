# app/schemas.py
from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional


# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Pydantic model for user response
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        dict = ConfigDict()
        from_attributes = True
