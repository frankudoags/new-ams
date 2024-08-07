from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from app.core.security import lecturer_guard, get_current_lecturer
from app import models, schemas
from app.core.db import db_dependency
from app.services.lecturer import (
    mark_attendance,
    view_lecturer_courses,
    create_attendance_session,
    get_students_for_course,
    get_course_attendance_no_of_students_present_for_each_class_and_no_of_classes_held as gcs,
)
from app.utils import check_face

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


@router.get(
    "/get_students_for_a_course",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.StudentWithAttendance],
)
async def get_course_students(
    course_id: int,
    db: db_dependency,
):
    students = get_students_for_course(db, course_id)
    return students


@router.get("/get_course_session_details", status_code=status.HTTP_200_OK)
async def get_course_session_details(
    course_id: int,
    db: db_dependency,
):
    return gcs(db, course_id)


@router.post(
    "/create_session",
    status_code=status.HTTP_200_OK,
)
async def create_session(
    course_id: int,
    title: str,
    db: db_dependency,
):
    session = create_attendance_session(db, course_id, title)
    if not session:
        raise HTTPException(status_code=400, detail="Session creation failed.")

    return {
        "message": "Attendance session created successfully.",
        "course_id": course_id,
    }


@router.post(
    "/mark_attendance",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AttendanceStudent,
)
async def mark_student_attendance(
    db: db_dependency,
    face: Annotated[UploadFile, File(...)],
    course_id: Annotated[int, Form(...)],
    class_date: Annotated[str, Form(...)],
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    students = course.students
    found, student = await check_face(face, students)

    if not found or not student:
        raise HTTPException(status_code=400, detail="Student not recognized.")

    id = student.id

    attendance = mark_attendance(db, course_id, id, class_date)
    if not attendance:
        raise HTTPException(
            status_code=400, detail="Attendance marking failed. check me"
        )

    student_with_attendance = schemas.AttendanceStudent(
        name=student.name, present=attendance.present
    )
    return student_with_attendance
