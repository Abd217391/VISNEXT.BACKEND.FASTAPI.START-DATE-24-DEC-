from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    department_id: int


class CourseResponse(BaseModel):
    id: int
    name: str
    department_id: int

    class Config:
        from_attributes = True
