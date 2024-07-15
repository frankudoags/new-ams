from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_student, student_guard
from app import schemas, models
from app.core.db import db_dependency
from app.services.student import (
    register_course,
    get_student_courses,
    get_student_attendance,
)

router = APIRouter(dependencies=[Depends(student_guard)])


@router.get("/profile", response_model=schemas.Student, status_code=status.HTTP_200_OK)
async def read_student_profile(
    db: db_dependency,
    current_user=Depends(get_current_student),
):
    return db.query(models.Student).filter(models.Student.id == current_user.id).first()


@router.get(
    "/courses", response_model=List[schemas.CourseData], status_code=status.HTTP_200_OK
)
async def read_student_courses(
    db: db_dependency,
    current_user=Depends(get_current_student),
):
    return get_student_courses(db, current_user.id)


@router.get(
    "/attendance",
    status_code=status.HTTP_200_OK,
)
async def read_student_attendance(
    db: db_dependency,
    course_id: int,
    current_user=Depends(get_current_student),
):
    return get_student_attendance(db, current_user.id, course_id)


@router.post(
    "/register_course",
    status_code=status.HTTP_201_CREATED,
)
async def register_student_course(
    course_id: int,
    db: db_dependency,
    current_user=Depends(get_current_student),
):
    course, error = register_course(db, course_id, current_user.id)
    if error:
        raise HTTPException(status_code=400, detail=error)

    return current_user, course