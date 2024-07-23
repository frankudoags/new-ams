from sqlalchemy.orm import Session
from app import models
import datetime


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


def mark_attendance(db: Session, course_id: int, student_id: int):
    attendance = (
        db.query(models.Attendance) # Get the attendance table
        .filter(models.Attendance.course_id == course_id) # Get the attendance record for the course
        .filter(models.Attendance.student_id == student_id) # Get the attendance record for the student
        .order_by(models.Attendance.timestamp.desc()) # Get the latest attendance session
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
    return course.students