from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.students.student_model import Student
from app.students.student_schema import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)
from app.departments.department_model import Department


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate,db: Session = Depends(get_db),):
    # Check if department exists
    department = (
        db.query(Department).filter(Department.id == student.department_id).first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

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


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = (db.query(Student).filter(Student.id == student_id).first())

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # If department_id is updated, validate it
    if student_data.department_id is not None:
        department = (db.query(Department).filter(Department.id == student_data.department_id).first())

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        student.department_id = student_data.department_id

    if student_data.name is not None:
        student.name = student_data.name

    if student_data.email is not None:
        student.email = student_data.email

    db.commit()
    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
