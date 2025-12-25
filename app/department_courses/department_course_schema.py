from pydantic import BaseModel


class DepartmentCourseCreate(BaseModel):
    department_id: int
    course_id: int


class DepartmentCourseResponse(BaseModel):
    id: int
    department_name: str
    course_name: str
