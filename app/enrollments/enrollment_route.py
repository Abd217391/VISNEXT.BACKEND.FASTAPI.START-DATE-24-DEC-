from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enrollments.enrollment_model import Enrollment
from app.enrollments.enrollment_schema import (
    EnrollmentCreate,
    EnrollmentResponse
)

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_enrollment(enrollment: EnrollmentCreate,db: Session = Depends(get_db)
):
    # Check duplicate enrollment
    existing = db.query(Enrollment).filter(Enrollment.student_id == enrollment.student_id,Enrollment.course_id == enrollment.course_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course"
        )

    new_enrollment = Enrollment(student_id=enrollment.student_id,course_id=enrollment.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment
