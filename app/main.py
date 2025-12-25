from fastapi import FastAPI

from app.database import Base, engine

from app.departments.department_route import router as department_router
from app.students.student_route import router as student_router
from app.courses.course_route import router as course_router
from app.enrollments.enrollment_route import router as enrollment_router
from app.department_courses.department_course_router import (
    router as department_course_router
)

app = FastAPI(title="University-Backend")


Base.metadata.create_all(bind=engine)


app.include_router(department_router)
app.include_router(student_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(department_course_router)


@app.get("/")
def root():
    return {"message": "University Backend Running"}
