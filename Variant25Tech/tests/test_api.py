from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_teaher():
    """
    Тест на создание нового учителя
    """
    response = client.post(
        "/teachers/",
        json={"teacher_name": "Наталья", "rank": "Глава", "degree": "Инженер", "department": "Информатика", "phone":"89505466756", "email": "Test@email.ru"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["teacher_name"] == "Наталья"
    assert data["rank"] == "Глава"
    assert data["degree"] == "Инженер"
    assert data["department"] == "Информатика"
    assert data["phone"] == "89505466756"
    assert data["email"] == "Test@email.ru"
    

def test_get_teachers():
    """
    Тест на получение списка Учителей из БД
    """
    response = client.get("/teachers/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["teacher_name"] == "Наталья"



def test_get_teaher_by_id():
    """
    Тест на получение Учителя из БД по его id
    """
    response = client.get("/teachers/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["teacher_name"] == "Наталья"


def test_teacher_not_found():
    """
    Проверка случая, если Учитель с таким id отсутствует в БД
    """
    response = client.get("/teachers/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Teacher not found"


def test_add_tems_to_teacher():
    """
    Тест на добавление Темы учителю
    """
    response = client.post(
        "/teachers/1/themes/",
        json={"diploma": "Написание отчета по ГОСТу"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["diploma"] == "Написание отчета по ГОСТу"
    assert data["teacher_id"] == 1


def test_get_tems():
    """
    Тест на получение списка Тем из БД
    """
    response = client.get("/themes/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["diploma"] == "Написание отчета по ГОСТу"
    assert data[0]["teacher_id"] == 1

def test_tems_not_found():
    """
    Проверка случая, если Тема с таким id отсутствует в БД
    """
    response = client.get("/themes/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Theme not found"

    

def test_create_student():
    """
    Тест на создание студента 
    """
    response = client.post(
        "/students/",
        json={"student_name": "Василиса", "faculty": "Информатика", "group": "1182б"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["student_name"] == "Василиса"
    assert data["faculty"] == "Информатика"
    assert data["group"] == "1182б"

def test_get_students():
    """
    Тест на получение списка Студентов из БД
    """
    response = client.get("/students/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["student_name"] == "Василиса"

def test_get_student_by_id():
    """
    Тест на получение Студента из БД по его id
    """
    response = client.get("/students/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["student_name"] == "Василиса"

def test_student_not_found():
    """
    Проверка случая, если Студент с таким id отсутствует в БД
    """
    response = client.get("/students/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Student not found"

def test_add_marks_to_student():
    """
    Тест на добавление Оценки Студенту
    """
    response = client.post(
        "/students/1/marks/",
        json={"gos_ex": "2", "def_ex": "3"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["student_id"] == 1
    assert data["gos_ex"] == 2
    assert data["def_ex"] == 3
    

def test_get_marks():
    """
    Тест на получение списка Оценок из БД
    """
    response = client.get("/marks/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["gos_ex"] == 2

def test_get_marks_by_id():
    """
    Тест на получение Оценки из БД по id
    """
    response = client.get("/marks/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["gos_ex"] == 2

def test_add_marks_to_student_not():
    """
    Тест если оценка уже есть у Студента
    """
    response = client.post(
        "/students/1/marks/",
        json={"gos_ex": "2", "def_ex": "3"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Mark student id already exist"

def test_get_Markss_by_id():
    """
    Тест на получение оценки из БД по id
    """
    response = client.get("/marks/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Mark not found"

def test_Sozdan_student():
    """
    Тест если студент уже создан 
    """
    response = client.post(
        "/students/",
        json={"student_name": "Василиса", "faculty": "Информатика", "group": "1182б"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Student name is already exist"

def test_sozdan_teaher():
    """
    Тест если учитель уже создан
    """
    response = client.post(
        "/teachers/",
        json={"teacher_name": "Наталья", "rank": "Глава", "degree": "Инженер", "department": "Информатика", "phone":"89505466756", "email": "Test@email.ru"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Teacher name is already exist"

