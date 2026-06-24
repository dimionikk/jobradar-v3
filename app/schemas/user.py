from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    stack: Optional[str] = None
    experience_years: Optional[int] = None
    salary_expectation: Optional[int] = None
    city: Optional[str] = None
    work_type: Optional[str] = None
    bio: Optional[str] = None
    resume_text: Optional[str] = None


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