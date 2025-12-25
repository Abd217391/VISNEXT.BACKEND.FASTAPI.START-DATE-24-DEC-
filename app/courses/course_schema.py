from pydantic import BaseModel
from typing import Optional


class CourseCreate(BaseModel):
    name: str
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    department_id: int

    class Config:
        from_attributes = True
