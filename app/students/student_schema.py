from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    department_id: int


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: int

    class Config:
        from_attributes = True
