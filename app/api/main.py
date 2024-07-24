from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.db import db_dependency
from app.api.routes import admin, lecturer, student
from app.core.security import create_access_token
from app.services.login import authenticate_user
from fastapi.security import OAuth2PasswordRequestForm


api_router = APIRouter()


@api_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data=user.__dict__)
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}


api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(lecturer.router, prefix="/lecturer", tags=["lecturer"])
api_router.include_router(student.router, prefix="/student", tags=["student"])
