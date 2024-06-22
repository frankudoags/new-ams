from fastapi import APIRouter

from app.api.routes import admin, lecturer, student

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(lecturer.router, prefix="/lecturer", tags=["lecturer"])
api_router.include_router(student.router, prefix="/student", tags=["student"])
