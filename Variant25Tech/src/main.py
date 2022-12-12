from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():

    db = SessionLocal() # pragma: no cover
    try:# pragma: no cover
        yield db# pragma: no cover
    finally:# pragma: no cover
        db.close()# pragma: no cover

@app.get("/teachers/", response_model=list[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers

@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher_by_id(teacher_id: int, db: Session = Depends(get_db)):

    db_teacher = crud.get_teacher_by_id(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):

    db_teacher = crud.get_teacher_by_name(db, teacher_name=teacher.teacher_name)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Teacher name is already exist")
    return crud.create_teacher(db=db, teacher=teacher)

@app.post("/teachers/{teacher_id}/themes/", response_model=schemas.Theme)
def create_item_for_user(teacher_id: int, theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    
    return crud.create_theme_teacher(db=db, theme=theme, teacher_id=teacher_id)


@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student_by_id(student_id: int, db: Session = Depends(get_db)):

    db_student = crud.get_student_by_id(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):

    db_student = crud.get_student_by_name(db, student_name=student.student_name)
    if db_student:
       raise HTTPException(status_code=400, detail="Student name is already exist")
    return crud.create_student(db=db, student=student)

@app.post("/students/{student_id}/marks/", response_model=schemas.Mark)
def create_mark_for_student(student_id: int, mark: schemas.MarkCreate, db: Session = Depends(get_db)):
    
    db_mark = crud.get_mark_by_student_id(db, student_id=student_id)
    if db_mark:
        raise HTTPException(status_code=404, detail="Mark student id already exist")
    return crud.create_mark_student(db=db, mark=mark, student_id=student_id)



@app.get("/themes/{theme_id}", response_model=schemas.Theme)
def read_theme_by_id(theme_id: int, db: Session = Depends(get_db)):

    db_theme = crud.get_theme_by_id(db, theme_id=theme_id)
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return db_theme  # pragma: no cover

@app.get("/themes/", response_model=list[schemas.Theme])
def read_themes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    themes = crud.get_themes(db, skip=skip, limit=limit)
    return themes


@app.get("/marks/{mark_id}", response_model=schemas.Mark)
def read_mark_by_id(mark_id: int, db: Session = Depends(get_db)):

    db_mark = crud.get_mark_by_id(db, mark_id=mark_id)
    if db_mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return db_mark

@app.get("/marks/", response_model=list[schemas.Mark])
def read_marks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    marks = crud.get_marks(db, skip=skip, limit=limit)
    return marks



