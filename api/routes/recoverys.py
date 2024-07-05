from fastapi import Depends, APIRouter
from api.schemas import sch_users as sch_user
from api.schemas.sch_users import LoginRequest
from sqlalchemy.orm import Session
from api.crud import crd_users as crd_user

from api.database import get_db


import api.utils.auth as auth

router = APIRouter()


@router.post("")
async def recovery_password(login: LoginRequest, db: Session = Depends(get_db)):

    user_email = login.email
    new_pass = login.password

    user = crd_user.update_password_by_email(db, user_email, new_pass)

    if user is None:
        return {"Detail": "No se hizo el cambio de contraseña"}

    return {"Detail": "Contraseña cambiada exitosamente"}
