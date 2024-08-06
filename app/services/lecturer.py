from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
import datetime
from app.services.student import get_student_attendance


def get_lecturer_by_email(db: Session, email: str):
    return db.query(models.Lecturer).filter(models.Lecturer.email == email).first()


def get_lecturer_by_id(db: Session, lecturer_id: int):
    return db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()


def view_lecturer_courses(db: Session, lecturer_id: int):
    lecturer = (
        db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()
    )
    return lecturer.courses


def create_attendance_session(db: Session, course_id: int) -> None:
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    students = course.students
    timestamp = datetime.datetime.now()
    attendance_records = [
        models.Attendance(
            course_id=course_id, student_id=student.id, timestamp=timestamp
        )
        for student in students
    ]
    db.add_all(attendance_records)
    db.commit()
    return True


def mark_attendance(db: Session, course_id: int, student_id: int, class_date: str):
    class_date_obj = datetime.datetime.fromisoformat(class_date)

    attendance = (
        db.query(models.Attendance)
        .filter(models.Attendance.course_id == course_id)
        .filter(models.Attendance.student_id == student_id)
        .filter(func.date(models.Attendance.timestamp) == class_date_obj.date())
        .first()
    )

    if attendance:
        attendance.present = True
        db.commit()
        db.refresh(attendance)
        return attendance
    else:
        return None


def get_students_for_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    students = course.students
    student_with_attendance_list = []

    for student in students:
        attendance_list = get_student_attendance(db, student.id, course_id)
        if attendance_list:
            total = len(attendance_list)
            sum_attendance = sum(a.present for a in attendance_list)
            print(sum_attendance, total)
            attendance_level = ceil((sum_attendance / total) * 100) if total else 0
        else:
            attendance_level = 0

        student_data = student.__dict__
        student_data["attendance_level"] = attendance_level

        student_with_attendance = schemas.StudentWithAttendance(**student_data)
        student_with_attendance_list.append(student_with_attendance)

    return student_with_attendance_list


def get_course_attendance_no_of_students_present_for_each_class_and_no_of_classes_held(
    db: Session, course_id: int
):
    # Query to get all attendance records for the specified course
    attendance_records = (
        db.query(
            models.Attendance.timestamp,
            func.count(models.Attendance.student_id)
            .filter(models.Attendance.present == True)
            .label("students_present"),
        )
        .filter(models.Attendance.course_id == course_id)
        .group_by(models.Attendance.timestamp)
        .all()
    )

    # Count the total number of classes held
    total_classes_held = len(attendance_records)

    # Query to get the total number of students enrolled in the course
    total_students = (
        db.query(func.count(models.CourseStudent.student_id))
        .filter(models.CourseStudent.course_id == course_id)
        .scalar()
    )

    # Prepare the result as a list of dictionaries
    result = []
    for record in attendance_records:
        result.append(
            {
                "class_date": record.timestamp,
                "students_present": record.students_present,
                "total_students": total_students,
                "attendance_ratio": f"{record.students_present}/{total_students}",
            }
        )

    return {
        "total_classes_held": total_classes_held,
        "total_students": total_students,
        "attendance_records": result,
    }
