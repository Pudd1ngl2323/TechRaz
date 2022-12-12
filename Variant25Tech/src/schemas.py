from pydantic import BaseModel
from datetime import date


class ThemeBase(BaseModel):
    diploma: str

class ThemeCreate(ThemeBase):
    pass

class Theme(ThemeBase):
    id: int
    teacher_id: int

    class Config:
        orm_mode = True




class MarkBase(BaseModel):
    gos_ex: int
    def_ex: int

class MarkCreate(MarkBase):
    pass

class Mark(MarkBase):
    id: int
    student_id: int
    class Config:
        orm_mode = True




class TeacherBase(BaseModel):
    teacher_name: str
    rank: str 
    degree: str 
    department: str
    phone: str
    email: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int
    theme: list[Theme] = []

    class Config:
        orm_mode = True




class StudentBase(BaseModel):
    student_name: str
    faculty: str
    group: str
    

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    mark: list[Mark] = []

    class Config:
        orm_mode = True



