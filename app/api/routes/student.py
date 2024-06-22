from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import student_guard

router = APIRouter(dependencies=[Depends(student_guard)])


@router.get("/")
def read_admin():
    return {"message": "Welcome, Student!"}
