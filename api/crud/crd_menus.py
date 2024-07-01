from api.schemas import sch_menus as sch_menu
from api.models import Menu as mod_menu
from sqlalchemy.orm import Session


def get_menu(db: Session, menu_id: int):
    return db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()


def get_menus(db: Session, skip: int = 0, limit: int = 10):
    return db.query(mod_menu).offset(skip).limit(limit).all()


def create_menu(db: Session, menu: sch_menu.MenuCreate):
    db_menu = mod_menu(**menu.model_dump())
    db_menu.status = True
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu_id: int, menu: sch_menu.MenuUpdate):
    db_menu = db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()
    if db_menu:
        for key, value in menu.model_dump().items():
            setattr(db_menu, key, value)
        db.commit()
        db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu
