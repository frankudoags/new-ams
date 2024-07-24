from pydantic import BaseModel
from enum import Enum
from typing import List

class EnumRole(str, Enum):
    ADMIN = "ADMIN"
    LECTURER = "LECTURER"
    STUDENT = "STUDENT"

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    role: EnumRole


class CreateStudent(CreateUser):
    matric_no: str
    facial_encoding: str


class CreateLecturer(CreateUser):
    pass

class CreateAdmin(CreateUser):
    pass


class CreateCourse(BaseModel):
    name: str
    code: str
    lecturer_id: int

class User(BaseModel):
    id: int
    name: str
    email: str
    role: EnumRole

class Student(User):
    matric_no: str

class StudentWithAttendance(Student):
    attendance_level: int

class StudentWithFaceEncoding(Student):
    facial_encoding: str


class Lecturer(User):
    pass
 
class Admin(User):
    pass

class Course(BaseModel):
    id: int
    name: str
    code: str
    lecturer_id: int
    lecturer: Lecturer
    students: List[Student]


class CourseData(BaseModel):
    id: int
    name: str
    code: str
    lecturer_id: int
    lecturer: Lecturer