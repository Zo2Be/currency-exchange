from datetime import timedelta
import logging
import re
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from sqlalchemy.orm import Session
from app.api.schemas.user import UserInput
from app.core.security import (
    create_jwt_token,
)
from app.core.config import Settings
from app.db.models import User
from app.db.database import get_db

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = Settings()
router = APIRouter()

PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

def verify_password(plain_password, hashed_password) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def get_password_hash(password):
    check_password = is_password_good(password)
    if check_password:
        return pwd_context.hash(password)
    return False


def is_password_good(password: str) -> bool:
    check_password: re.Match[str] | None = re.match(PASSWORD_PATTERN, password)
    if not check_password:
        return False
    return True


def get_user_from_db(db: Session, username: str) -> Any:
    return db.query(User).filter(User.username == username).first()


@router.post("/register/")
def registration(
    user_in: UserInput, db: Session = Depends(get_db),
) -> dict[str, str] | None:
    user_data_from_db: UserInput | None = get_user_from_db(db, user_in.username)
    hash_password = get_password_hash(user_in.password)

    if not user_data_from_db and hash_password:
        new_user = User(username=user_in.username, hashed_password=hash_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info("User %s registered successfully", user_in.username)
        return {"message": f"Welcome to the club, {user_in.username}"}

    if user_data_from_db:
        logger.warning("User %s already exists", user_in.username)
        return {"error": "A user with this same name already exists"}

    if not hash_password:
        logger.warning("Password %s does not meet the requirements", user_in.username)
        return {
            "message": "1. Has minimum 8 characters in length. "
            "2. At least one uppercase English letter. "
            "3. At least one lowercase English letter. "
            "4. At least one digit. "
            "5. At least one special character."
        }
    return NotImplemented


@router.post("/login/")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> dict[str, str]:
    user_data_from_db = get_user_from_db(db, user_data.username)
    password: bool = verify_password(user_data.password, user_data_from_db.hashed_password)
    if user_data_from_db is None or not password:
        logger.error("Invalid login attempt for user %s", user_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token: str = create_jwt_token(
        {"sub": user_data.username}, expires_delta=access_token_expires
    )
    logger.info("User %s logged in successfully", user_data.username)
    return {"access_token": access_token, "token_type": "bearer"}
