from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class DepartmentCourse(Base):
    __tablename__ = "department_courses"

    id = Column(Integer, primary_key=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    department = relationship("Department")
    course = relationship("Course")

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "course_id",
            name="unique_department_course"
        ),
    )
