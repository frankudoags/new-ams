from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.core.security import get_password_hash


def create_new_admin(db: Session, admin: schemas.CreateAdmin) -> models.Admin:
    new_admin = models.Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=get_password_hash(admin.password),
        role=admin.role,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def create_new_student(
    db: Session, name, email, password, matric_no, facial_encoding
) -> models.Student:
    new_student = models.Student(
        name=name,
        email=email,
        hashed_password=get_password_hash(password),
        role="STUDENT",
        matric_no=matric_no,
        facial_encoding=facial_encoding,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def create_new_lecturer(
    db: Session, lecturer: schemas.CreateLecturer
) -> models.Lecturer:
    new_lecturer = models.Lecturer(
        name=lecturer.name,
        email=lecturer.email,
        hashed_password=get_password_hash(lecturer.password),
        role=lecturer.role,
    )
    db.add(new_lecturer)
    db.commit()
    db.refresh(new_lecturer)
    return new_lecturer


def create_new_course(db: Session, course: schemas.CreateCourse) -> models.Course:
    new_course = models.Course(
        name=course.name, code=course.code, lecturer_id=course.lecturer_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
