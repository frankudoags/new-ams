from fastapi import APIRouter, File, HTTPException, status, Depends, UploadFile, Form
from typing import Annotated
from app.core.db import db_dependency
from app.core.security import admin_guard
from app import schemas, models
from app.services.admin import (
    create_new_admin,
    create_new_student,
    create_new_lecturer,
    create_new_course,
)
from app.utils import get_face_encodings


router = APIRouter(dependencies=[Depends(admin_guard)])


@router.post(
    "/create_admin", response_model=schemas.Admin, status_code=status.HTTP_201_CREATED
)
async def create_admin(admin: schemas.CreateAdmin, db: db_dependency):
    admin = create_new_admin(db, admin)
    if not admin:
        raise HTTPException(status_code=400, detail="Admin creation failed.")

    return admin


@router.post(
    "/create_student",
    response_model=schemas.Student,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    db: db_dependency,
    face: Annotated[UploadFile, File()],
    name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    matric_no: Annotated[str, Form(...)],
):
    facial_encoding = await get_face_encodings(face)
    student = create_new_student(db, name, email, password, matric_no, facial_encoding)
    if not student:
        raise HTTPException(status_code=400, detail="Student creation failed.")

    return student


@router.post(
    "/create_lecturer",
    response_model=schemas.Lecturer,
    status_code=status.HTTP_201_CREATED,
)
async def create_lecturer(lecturer: schemas.CreateLecturer, db: db_dependency):
    lecturer = create_new_lecturer(db, lecturer)
    if not lecturer:
        raise HTTPException(status_code=400, detail="Lecturer creation failed.")

    return lecturer


@router.post(
    "/create_course", response_model=schemas.Course, status_code=status.HTTP_201_CREATED
)
async def create_course(course: schemas.CreateCourse, db: db_dependency):
    course = create_new_course(db, course)
    if not course:
        raise HTTPException(status_code=400, detail="Course creation failed.")

    return course


@router.get(
    "/lecturers", response_model=list[schemas.Lecturer], status_code=status.HTTP_200_OK
)
async def get_lecturers(db: db_dependency):
    lecturers = db.query(models.Lecturer).all()
    return lecturers


@router.get(
    "/students", response_model=list[schemas.Student], status_code=status.HTTP_200_OK
)
async def get_students(db: db_dependency):
    students = db.query(models.Student).all()
    return students


@router.get(
    "/courses", response_model=list[schemas.Course], status_code=status.HTTP_200_OK
)
async def get_courses(db: db_dependency):
    courses = db.query(models.Course).all()
    return courses


@router.post("/encode_face")
async def encode_face(file: UploadFile = File(...)):
    face = await get_face_encodings(file)
    return face
