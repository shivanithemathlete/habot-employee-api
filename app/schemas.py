from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: Optional[str]
    role: Optional[str]
    date_joined: date

    class Config:
        from_attributes = True
