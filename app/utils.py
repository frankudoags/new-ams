import json
from face_recognition import (
    load_image_file,
    face_encodings,
    compare_faces,
    face_locations,
)
from fastapi import UploadFile
from app.schemas import StudentWithFaceEncoding
from typing import List


async def get_face_encodings(file: UploadFile):
    image = load_image_file(file.file)
    boxes = face_locations(image, model="hog")
    face_encoding = json.dumps(face_encodings(image, boxes)[0].tolist())
    return face_encoding


async def check_face(file: UploadFile, students: List[StudentWithFaceEncoding]):
    image = load_image_file(file.file)
    boxes = face_locations(image, model="hog")
    face_encodings_list = face_encodings(image, boxes)

    if not face_encodings_list:
        return False, None

    face_encoding = face_encodings_list[0]

    known_faces = []

    for student in students:
        student_encoding = json.loads(student.facial_encoding)
        known_faces.append(student_encoding)


    matches = compare_faces(known_faces, face_encoding, 0.4)
    print(matches)
    if True in matches:
        match_index = matches.index(True)
        student = students[match_index]
        return True, student

    return False, None
