from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.departments.department_model import Department
from app.departments.department_schema import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post("/", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate,db: Session = Depends(get_db),):
    db_department = Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int,department: DepartmentUpdate,db: Session = Depends(get_db),
):
    db_department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not db_department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db_department.name = department.name
    db.commit()
    db.refresh(db_department)

    return db_department
