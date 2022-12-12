from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"# pragma: no cover

class Student(BaseModel):
    __tablename__ = "students"

    student_name = Column(String, unique=True, index=True)
    faculty = Column(String)
    group = Column(String)
       
    mark = relationship("Mark", back_populates="student") 

 
class Theme(BaseModel):
    __tablename__ = "themes"

    diploma = Column(String, unique=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    teacher = relationship("Teacher", back_populates="theme") 
    

class Mark(BaseModel):
    __tablename__ = "marks"
    
    gos_ex = Column(Integer)
    def_ex = Column(Integer)
    
    student_id = Column(Integer, ForeignKey("students.id"))

    student = relationship("Student", back_populates="mark") 

class Teacher(BaseModel):
    __tablename__ = "teachers"

    teacher_name = Column(String)
    rank = Column(String)
    degree = Column(String)
    department = Column(String)
    phone = Column(String)
    email = Column(String)

    theme = relationship("Theme", back_populates="teacher") 
