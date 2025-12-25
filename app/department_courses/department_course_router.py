from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.department_courses.department_course_model import DepartmentCourse
from app.departments.department_model import Department
from app.courses.course_model import Course
from app.department_courses.department_course_schema import (
    DepartmentCourseCreate,
    DepartmentCourseResponse,
)

router = APIRouter(
    prefix="/department-courses",
    tags=["Department Courses"],
)


# -------------------------
# ASSIGN COURSE TO DEPARTMENT
# -------------------------
@router.post("/", response_model=DepartmentCourseResponse)
def assign_course_to_department(
    data: DepartmentCourseCreate,
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(
        Department.id == data.department_id
    ).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(DepartmentCourse).filter(
        DepartmentCourse.department_id == data.department_id,
        DepartmentCourse.course_id == data.course_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Course already assigned"
        )

    department_course = DepartmentCourse(
        department_id=data.department_id,
        course_id=data.course_id,
    )

    db.add(department_course)
    db.commit()
    db.refresh(department_course)

    # ✅ RETURN WHAT THE RESPONSE MODEL EXPECTS
    return {
        "id": department_course.id,
        "department_name": department.name,
        "course_name": course.name,
    }


# -------------------------
# REMOVE COURSE FROM DEPARTMENT
# -------------------------
@router.delete("/{department_course_id}")
def remove_course_from_department(
    department_course_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(DepartmentCourse)
        .filter(DepartmentCourse.id == department_course_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {"message": "Course removed from department successfully"}
