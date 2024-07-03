from fastapi import Depends, APIRouter, HTTPException, status
from api.schemas.sch_users import LoginRequest
from api.schemas.sch_tokens import Token
from sqlalchemy.orm import Session

from api.database import get_db
from datetime import timedelta


import api.utils.auth as auth

router = APIRouter()


@router.post("", response_model=Token)
async def login_for_access_token(login: LoginRequest, db: Session = Depends(get_db)):

    user = auth.authenticate_user(db, login.email, login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"email": user.email, "type": user.id_user_type},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token}
