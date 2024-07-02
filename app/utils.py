import json
from face_recognition import (
    load_image_file,
    face_encodings,
    compare_faces,
    face_locations,
)
from fastapi import UploadFile
from app.schemas import StudentWithFaceEncoding

async def get_face_encodings(file: UploadFile):
    image = load_image_file(file.file)
    boxes = face_locations(image, model="hog")
    face_encoding = json.dumps(face_encodings(image, boxes)[0].tolist())
    return face_encoding


async def check_face(file: UploadFile, students: list[StudentWithFaceEncoding]):
    image = load_image_file(file.file)
    boxes = face_locations(image, model="hog")
    face_encoding = face_encodings(image, boxes)

    found = False
    student = None

    for student in students:
        student_encoding = json.loads(student.face_encoding)
        if compare_faces(student_encoding, face_encoding)[0]:
            found = True
            student = student
            break
    
    return found, student
