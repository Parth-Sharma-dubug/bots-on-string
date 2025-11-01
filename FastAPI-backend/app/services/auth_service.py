from datetime import timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.security import create_access_token
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === Password Utilities ===
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# === Token Generation ===
def create_login_token(user_id: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
    )
    return token
