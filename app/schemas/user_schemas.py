# app/schemas.py
from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional


class SignInRequest(BaseModel):
    username: str
    password: str

# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


# Pydantic model for user response
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str 

    class Config:
        orm_mode = True

# Schema for user login
class UserLogin(BaseModel):
    email: str
    password: str
    role:str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int 
    role: str

# Schema for token data
class TokenData(BaseModel):
    username: str
    role: str 
