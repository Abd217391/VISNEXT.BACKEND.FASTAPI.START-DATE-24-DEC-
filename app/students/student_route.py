from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.students.student_model import Student
from app.students.student_schema import StudentCreate, StudentResponse
from app.departments.department_model import Department

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    # check if department exists
    department = db.query(Department).filter(
        Department.id == student.department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    db_student = Student(
        name=student.name,
        email=student.email,
        department_id=student.department_id
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
