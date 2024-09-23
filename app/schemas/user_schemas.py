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
        orm_mode = True

# Schema for user login
class UserLogin(BaseModel):
    email: str
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    username: str
