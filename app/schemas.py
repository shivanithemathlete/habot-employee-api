from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
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
