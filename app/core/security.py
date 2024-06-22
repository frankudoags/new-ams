from datetime import datetime, timedelta
from typing import Any
from app import models
from fastapi import Depends, HTTPException, status

# import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"
SECRET_KEY = "ff0b4ab3e2b00da6d35d1ae2fec6de76468c861b"


# def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
#     expire = datetime.now(datetime.UTC) + expires_delta
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user() -> models.User:
    return models.User(
        id=1,
        name="test",
        email="test@gmail.com",
        role="ADMIN"
    )



def admin_guard(current_user = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation."
        )

def lecturer_guard(current_user = Depends(get_current_user)):
    pass
    # if current_user.role != "LECTURER":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="You are not authorized to perform this operation."
    #     )

def student_guard(current_user = Depends(get_current_user)):
    pass
    # if current_user.role != "STUDENT":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="You are not authorized to perform this operation."
    #     )