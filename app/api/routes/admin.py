from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import db_dependency
from app.core.security import admin_guard
from app import schemas
from app.services.admin import (
    create_new_admin,
    create_new_student,
    create_new_lecturer,
    create_new_course,
)

router = APIRouter(dependencies=[Depends(admin_guard)])


@router.post(
    "/create_admin", response_model=schemas.Admin, status_code=status.HTTP_201_CREATED
)
async def create_admin(admin: schemas.CreateAdmin, db: db_dependency):
    admin =  create_new_admin(db, admin)
    if not admin:
        raise HTTPException(status_code=400, detail="Admin creation failed.")
    
    return admin


@router.post(
    "/create_student", response_model=schemas.Student, status_code=status.HTTP_201_CREATED
)
async def create_student(student: schemas.CreateStudent, db: db_dependency):
    student = create_new_student(db, student)
    if not student:
        raise HTTPException(status_code=400, detail="Student creation failed.")
    
    return student



@router.post(
    "/create_lecturer", response_model=schemas.Lecturer, status_code=status.HTTP_201_CREATED
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
