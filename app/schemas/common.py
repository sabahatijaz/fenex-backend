# app/common.py
from pydantic import BaseModel, EmailStr,ConfigDict, Field
from typing import Optional


class BasicResponse(BaseModel):
    success: bool = Field(..., example=True)
    reason : str = Field(None, example="Data updated successfully")