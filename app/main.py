from fastapi import FastAPI
from app.students.student_route import router as student_router
from app.courses.course_route import router as course_router




from app.database import Base, engine
from app.departments.department_route import router as department_router

app = FastAPI(title="University Backend")

Base.metadata.create_all(bind=engine)


app.include_router(course_router)

app.include_router(department_router)
app.include_router(student_router)


@app.get("/")
def root():
    return {"message": "University Backend Running"}
