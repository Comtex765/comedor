from api.schemas import sch_users as sch_user
from api.models import User as mod_user
from sqlalchemy.orm import Session
from datetime import datetime

import bcrypt


def get_user_by_id(db: Session, user_id: int):
    return db.query(mod_user).filter(mod_user.id_user == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(mod_user).filter(mod_user.email == email).first()


def get_user_cellphone(db: Session, cell: str):
    return db.query(mod_user).filter(mod_user.cellphone == cell).first()


def get_user_cedula(db: Session, ced: str):
    return db.query(mod_user).filter(mod_user.cedula == ced).first()


def get_users(db: Session):
    return db.query(mod_user).all()


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
    return db_user


def update_user(db: Session, user_id: int, user: sch_user.UserUpdate):
    db_user = db.query(mod_user).filter(mod_user.id_user == user_id).first()
    if db_user:
        if user.hash_password:
            db_user.hash_password = bcrypt.hashpw(
                user.hash_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
