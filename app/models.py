from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Admin, Lecturer, Student


class Admin(User):
    __tablename__ = "admins"

    id = Column(ForeignKey("users.id"), primary_key=True)


class Student(User):
    __tablename__ = "students"

    id = Column(ForeignKey("users.id"), primary_key=True)
    matric_no = Column(String, unique=True, nullable=False)  # Matriculation number of the student
    facial_encoding = Column(String)  # Encoded facial features for recognition
    courses = relationship("Course", secondary="course_students", back_populates="students")  # Courses the student is taking


class Lecturer(User):
    __tablename__ = "lecturers"

    id = Column(ForeignKey("users.id"), primary_key=True) 
    courses = relationship("Course", back_populates="lecturer") # Lecturer's courses


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Name of the course
    code = Column(String, unique=True, nullable=False) # Unique course code
    lecturer_id = Column(ForeignKey("lecturers.id"), nullable=False) # id of the lecturer teaching the course
    lecturer = relationship("Lecturer", back_populates="courses") # The lecturer teaching the course
    students = relationship("Student", secondary="course_students", back_populates="courses") # Students taking the course


class CourseStudent(Base):
    __tablename__ = "course_students"

    course_id = Column(ForeignKey("courses.id"), primary_key=True)
    student_id = Column(ForeignKey("students.id"), primary_key=True)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)   # Time the attendance was marked
    title = Column(String, nullable=False)
    course_id = Column(ForeignKey("courses.id"), nullable=False)
    student_id = Column(ForeignKey("students.id"), nullable=False)
    present = Column(Boolean, nullable=False, default=False)  # True if student was present, False otherwise
