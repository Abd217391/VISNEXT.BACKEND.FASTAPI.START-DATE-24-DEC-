from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.courses.course_model import Course
from app.courses.course_schema import CourseCreate, CourseResponse

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# -------------------------
# CREATE COURSE (POST)
# -------------------------
@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    existing_course = db.query(Course).filter(
        Course.name == course.name,
        Course.department_id == course.department_id
    ).first()

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already exists in this department"
        )

    new_course = Course(
        name=course.name,
        department_id=course.department_id
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
