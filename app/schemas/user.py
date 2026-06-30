from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=254)
    password: str = Field(max_length=128)


class UserUpdate(BaseModel):
    stack: Optional[str] = Field(default=None, max_length=200)
    experience_years: Optional[int] = Field(default=None, ge=0, le=60)
    salary_expectation: Optional[int] = Field(default=None, ge=0)
    city: Optional[str] = Field(default=None, max_length=100)
    work_type: Optional[str] = Field(default=None, max_length=50)
    bio: Optional[str] = Field(default=None, max_length=2000)
    resume_text: Optional[str] = Field(default=None, max_length=10000)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    stack: Optional[str] = None
    experience_years: Optional[int] = None
    salary_expectation: Optional[int] = None
    city: Optional[str] = None
    work_type: Optional[str] = None
    bio: Optional[str] = None
    resume_text: Optional[str] = None
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)