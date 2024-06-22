from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import lecturer_guard

router = APIRouter(dependencies=[Depends(lecturer_guard)])


@router.get("/")
def read_admin():
    return {"message": "Welcome, Lecturer!"}
