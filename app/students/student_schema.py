from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    department_id: int


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: int

    class Config:
        from_attributes = True
