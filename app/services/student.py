from typing import List
from sqlalchemy.orm import Session
from app import models


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def register_course(db: Session, course_id: int, student_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not course or not student:
        return None, "Course or Student not found."

    # Check if student is already enrolled (optional)
    existing_enrollment = db.query(models.CourseStudent).filter(
        models.CourseStudent.course_id == course_id, models.CourseStudent.student_id == student_id
    ).first()

    if existing_enrollment:
        return None, "Student already enrolled in the course."
    
    # Create an association record in CourseStudent
    course_student = models.CourseStudent(course_id=course_id, student_id=student_id)
    db.add(course_student)
    db.commit()
    db.refresh(course_student)
    return course_student, None

def get_student_courses(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    return student.courses

def get_student_attendance(db: Session, student_id: int, course_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course or not student:
        return None, "Course or Student not found."

    attendance = db.query(models.Attendance).filter(
        models.Attendance.course_id == course_id, models.Attendance.student_id == student_id
    ).all()
    return attendance
