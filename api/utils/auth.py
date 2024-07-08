from api.crud.crd_users import get_only_user_by_email
from fastapi.security import OAuth2PasswordBearer
from api.schemas import sch_tokens as sch_token
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from colorama import Fore, Style
from api.database import get_db
from dotenv import load_dotenv
from typing import Optional

import bcrypt
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def authenticate_user(db: Session, email: str, password: str):
    user = get_only_user_by_email(db, email)
    if not user or not verify_password(password, user.hash_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + timedelta(days=30) + expires_delta
    else:
        expire = datetime.now() + timedelta(days=30) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        type: int = payload.get("type")
        if email is None or type is None:
            raise credentials_exception
        token_data = sch_token.TokenData(email=email, type=type)
    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL}     💔    Error en lo del token: {e}  💔\n"
        )

    user = get_only_user_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception
    return user
