from datetime import datetime, timedelta
from typing import Any
from app import models
from fastapi import Depends, HTTPException, status
from app.core.db import db_dependency
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"
SECRET_KEY = "ff0b4ab3e2b00da6d35d1ae2fec6de76468c861b"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000 #change to 30 mins, used 3000 mins for testing


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = {
        "email": data.get("email")
    }
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(
      db: db_dependency,
    token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired, please login again",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("email")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise expired_credentials_exception
    except JWTError:
        raise credentials_exception

    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def admin_guard(current_user=Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation.",
        )


def lecturer_guard(current_user=Depends(get_current_user)):
    if current_user.role != "LECTURER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation.",
        )


def student_guard(current_user=Depends(get_current_user)):
    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation.",
        )


def get_current_student(
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> models.Student:
    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation.",
        )
    return db.query(models.Student).filter(models.Student.id == current_user.id).first()


def get_current_lecturer(
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> models.Lecturer:
    if current_user.role != "LECTURER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this operation.",
        )
    return (
        db.query(models.Lecturer).filter(models.Lecturer.id == current_user.id).first()
    )
