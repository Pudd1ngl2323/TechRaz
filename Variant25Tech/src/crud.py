from sqlalchemy.orm import Session

from src import models, schemas

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(teacher_name=teacher.teacher_name, rank=teacher.rank, degree=teacher.degree, department=teacher.department, phone=teacher.phone, email=teacher.email)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(student_name=student.student_name, faculty=student.faculty, group=student.group)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_mark_student(db: Session, mark: schemas.MarkCreate, student_id: int):
    db_mark = models.Mark(**mark.dict(), student_id=student_id)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


def create_theme_teacher(db: Session, theme: schemas.ThemeCreate,  teacher_id: int):
    db_theme = models.Theme(**theme.dict(), teacher_id=teacher_id)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme



def get_teacher_by_id(db: Session, teacher_id: int):

    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def get_student_by_id(db: Session, student_id: int):

    return db.query(models.Student).filter(models.Student.id == student_id).first() 

def get_mark_by_id(db: Session, mark_id: int):
 
    return db.query(models.Mark).filter(models.Mark.id == mark_id).first()

def get_theme_by_id(db: Session, theme_id: int):
    return db.query(models.Theme).filter(models.Theme.id == theme_id).first()



def get_teacher_by_name(db: Session, teacher_name: str):
    return db.query(models.Teacher).filter(models.Teacher.teacher_name == teacher_name).first()


def get_student_by_name(db: Session, student_name: str):
    return db.query(models.Student).filter(models.Student.student_name == student_name).first()


def get_mark_by_student_id(db: Session, student_id: int):
    return db.query(models.Mark).filter(models.Mark.student_id == student_id).first()


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_themes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Theme).offset(skip).limit(limit).all()


def get_marks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mark).offset(skip).limit(limit).all()