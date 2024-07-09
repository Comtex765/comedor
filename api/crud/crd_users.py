from api.email.account_creating import send_email
from api.models import UserType as mod_user_type
from api.schemas import sch_users as sch_user
from api.models import User as mod_user
from sqlalchemy.orm import Session

from datetime import datetime

import bcrypt


def convert_user_to_user_with_type(user):
    if not user:
        return None

    return sch_user.UserWithType(
        user=sch_user.UserOut(**user.__dict__),
        type=sch_user.UserType(**user.user_type.__dict__),
    )


def get_user_by_id(db: Session, user_id: int):
    user = (
        db.query(mod_user)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .filter(mod_user.id_user == user_id)
        .first()
    )

    return convert_user_to_user_with_type(user)


def get_user_discount(db: Session, user_id: int):
    user = db.query(mod_user).filter(mod_user.id_user == user_id).first()

    discount = (
        db.query(mod_user_type)
        .filter(mod_user_type.id_user_type == user.id_user_type)
        .first()
    )

    return discount.percent_discount


def get_user_by_email(db: Session, email: str):
    user = (
        db.query(mod_user)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .filter(mod_user.email == email)
        .first()
    )

    return convert_user_to_user_with_type(user)


def get_only_user_by_email(db: Session, email: str):
    user = db.query(mod_user).filter(mod_user.email == email).first()

    return user


def get_only_balance_by_id(db: Session, user_id: int):
    user = db.query(mod_user).filter(mod_user.id_user == user_id).first()

    if user:
        return user.balance

    return None


def get_user_id_by_email(db: Session, email: str):
    user = (
        db.query(mod_user)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .filter(mod_user.email == email)
        .first()
    )

    return user.id_user


def get_user_by_cellphone(db: Session, cell: str):
    user = (
        db.query(mod_user)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .filter(mod_user.cellphone == cell)
        .first()
    )

    return convert_user_to_user_with_type(user)


def get_user_cedula(db: Session, ced: str):
    user = (
        db.query(mod_user)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .filter(mod_user.cedula == ced)
        .first()
    )

    return convert_user_to_user_with_type(user)


def get_users(db: Session):
    results = (
        db.query(mod_user, mod_user_type)
        .join(mod_user_type, mod_user.id_user_type == mod_user_type.id_user_type)
        .all()
    )

    response = [
        sch_user.UserWithType(
            user=sch_user.UserOut.model_validate(user),
            type=sch_user.UserType.model_validate(user_type),
        )
        for user, user_type in results
    ]

    return response


def create_user(db: Session, user: sch_user.UserCreate):
    hashed_password = bcrypt.hashpw(
        user.hash_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    db_user = mod_user(
        user_name=user.user_name,
        id_user_type=user.id_user_type,
        user_last_name=user.user_last_name,
        email=user.email,
        hash_password=hashed_password,
        cellphone=user.cellphone,
        balance=0,
        created_date=datetime.now(),
        cedula=user.cedula,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_email(db_user.email, db_user.user_name + " " + db_user.user_last_name)

    return db_user


def update_user(db: Session, user_id: int, user: sch_user.UserUpdate):
    db_user = db.query(mod_user).filter(mod_user.id_user == user_id).first()

    if db_user:
        for field, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
    return db_user


def update_balance(db: Session, user_id: int, balance: float):
    db_user = db.query(mod_user).filter(mod_user.id_user == user_id).first()

    if db_user:
        db_user.balance = float(balance) + float(db_user.balance)
        db.commit()
        db.refresh(db_user)
        return db_user

    return None


def delete_user(db: Session, user_id: int):
    db_user = db.query(mod_user).filter(mod_user.id_reservation == user_id).first()
    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


def update_password_by_email(db: Session, email: str, password: str):

    # Buscar al usuario por email
    user = get_only_user_by_email(db=db, email=email)

    if user is None:
        return None

    # Actualizar la contraseña
    user.set_password(password)

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(user)

    return user
