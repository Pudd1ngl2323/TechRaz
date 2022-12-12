"""empty message

Revision ID: first_data
Revises: 79fc262c1bf4
Create Date: 2022-11-30 03:11:36.386192

"""
from alembic import op
from sqlalchemy import orm

from src.models import Theme, Student, Teacher, Mark
# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '79fc262c1bf4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    teacher1 = Teacher(teacher_name='Антонина Ивановна', rank='Доктор наук', degree="Профессор", department='Исторический', phone="+7(565)1234567", email="annedu@mail.ru")
    teacher2 = Teacher(teacher_name='Гаранин Алексей', rank='Старший преподаватель', degree="", department='Экономический', phone="+7(898)1111111", email="garanin@gmail.com")
    
    session.add_all([teacher1, teacher2])
    session.flush()

    student1 = Student(student_name='Андрей Миронов', faculty='Экономический', group="4411a")
    student2 = Student(student_name='Ярослав Конев', faculty='Филологический', group="2133a")
    student3 = Student(student_name='Анна Жикина', faculty='Юридический', group="4001б")
    student4 = Student(student_name='Евгения Фырова', faculty='Исторический', group="1509б")
    

    session.add_all([student1, student2, student3, student4])
    session.flush()

    theme1 = Theme(diploma='Государственный строй эпохи Петра I, сословная реформа', teacher_id=teacher1.id)
    theme2 = Theme(diploma='Безработица и занятость', teacher_id=teacher2.id)
    theme3 = Theme(diploma='Становление и развитие экологического законодательства субъектов Российской Федерации', teacher_id=teacher1.id)
    theme4 = Theme(diploma='Разработка админки для сайта университета', teacher_id=teacher2.id)
   

    session.add_all([theme1, theme2, theme3, theme4])
    session.commit()

    mark1 = Mark(gos_ex=5, def_ex=3, student_id = student1.id)
    mark2 = Mark(gos_ex=3, def_ex=4, student_id = student2.id)
    mark3 = Mark(gos_ex=4, def_ex=5, student_id = student4.id)
    mark4 = Mark(gos_ex=4, def_ex=2, student_id = student3.id)
    

    session.add_all([mark1, mark2, mark3, mark4])
    session.commit()


def downgrade() -> None:
    pass
