from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    department_id = Column(Integer,ForeignKey("departments.id"),nullable=False
    )
