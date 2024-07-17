from api.schemas.sch_users import LoginRequest
from api.crud import crd_users as crd_user
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import get_db


router = APIRouter()


@router.post("")
async def recovery_password(login: LoginRequest, db: Session = Depends(get_db)):

    user_email = login.email
    new_pass = login.password

    user = crd_user.update_password_by_email(db, user_email, new_pass)

    if user is None:
        return {"detail": "No se hizo el cambio de contraseña"}

    return {"detail": "Contraseña cambiada exitosamente"}
