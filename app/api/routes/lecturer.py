from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import lecturer_guard, get_current_lecturer
from app import schemas
from app.core.db import db_dependency
from app.services.lecturer import (
    view_lecturer_courses,
    create_attendance_session,
    mark_attendance,
)

router = APIRouter(dependencies=[Depends(lecturer_guard)])


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=schemas.Lecturer)
async def read_lecturer_profile(
    current_user=Depends(get_current_lecturer),
):
    return current_user


@router.get(
    "/courses",
    response_model=list[schemas.Course],
    status_code=status.HTTP_200_OK,
)
async def read_lecturer_courses(
    db: db_dependency,
    current_user=Depends(get_current_lecturer),
):
    return view_lecturer_courses(db, current_user.id)


@router.post(
    "/create_session",
    status_code=status.HTTP_201_CREATED,
)
async def create_session(
    course_id: int,
    db: db_dependency,
):
    session = create_attendance_session(db, course_id)
    if not session:
        raise HTTPException(status_code=400, detail="Session creation failed.")

    return {
        "message": "Attendance session created successfully.",
        "course_id": course_id,
    }


@router.post(
    "/mark_attendance",
    status_code=status.HTTP_201_CREATED,
)
async def mark_student_attendance(
    course_id: int,
    student_id: int,
    db: db_dependency,
):
    attendance = mark_attendance(db, course_id, student_id)
    if not attendance:
        raise HTTPException(status_code=400, detail="Attendance marking failed.")

    return attendance