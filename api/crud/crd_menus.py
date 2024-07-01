from api.models import MealTime as mod_meal_time
from api.models import MenuType as mod_menu_type
from api.schemas import sch_menus as sch_menu
from api.models import Menu as mod_menu
from sqlalchemy.orm import Session


def get_menu(db: Session, menu_id: int):
    return db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()


def get_menus(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuTypeBase.model_validate(menu_type),
            meal_time=sch_menu.MealTimeBase.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


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
