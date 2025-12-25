from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.courses.course_model import Course
from app.courses.course_schema import CourseCreate, CourseResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.courses.course_model import Course
from app.courses.course_schema import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
)
from app.departments.department_model import Department




router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post( "/",response_model=CourseResponse,status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    existing_course = db.query(Course).filter(Course.name == course.name,Course.department_id == course.department_id).first()

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already exists in this department"
        )

    new_course = Course(name=course.name,department_id=course.department_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


# -------------------------
# GET ALL COURSES
# -------------------------
@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()



@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int,course_data: CourseUpdate,db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    

    # If department_id is being updated, check if department exists
    if course_data.department_id is not None:
        department = db.query(Department).filter(Department.id == course_data.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        course.department_id = course_data.department_id

    if course_data.name is not None:
        course.name = course_data.name

    db.commit()
    db.refresh(course)

    return course



@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()

    return None
