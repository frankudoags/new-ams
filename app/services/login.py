from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.core.security import get_password_hash, verify_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user