from api.models import DiningReservation as mod_dining
from api.models import MealTime as mod_meal_time
from api.models import MenuType as mod_menu_type
from api.schemas import sch_menus as sch_menu
from api.models import Menu as mod_menu
from sqlalchemy.orm import Session


def convert_menu_to_menu_with_time_type(menu):
    if not menu:
        return None

    return sch_menu.MenuWithTypeTime(
        menu=sch_menu.MenuOut(**menu.__dict__),
        menu_type=sch_menu.MenuType(**menu.menu_type.__dict__),
        meal_time=sch_menu.MealTime(**menu.meal_time.__dict__),
    )


def get_menu_by_id(db: Session, menu_id: int):
    menu = (
        db.query(mod_menu)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .filter(mod_menu.id_menu == menu_id)
        .first()
    )

    return convert_menu_to_menu_with_time_type(menu)


def get_menu_price(db: Session, menu_id: int):
    menu = db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()

    return menu.price


def get_menus(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .filter(mod_menu.status == True)
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuType.model_validate(menu_type),
            meal_time=sch_menu.MealTime.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


def get_all_menus(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuType.model_validate(menu_type),
            meal_time=sch_menu.MealTime.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


def get_all_desayunos(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .filter(mod_meal_time.meal_time == "Desayuno")
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuType.model_validate(menu_type),
            meal_time=sch_menu.MealTime.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


def get_all_almuerzos(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .filter(mod_meal_time.meal_time == "Almuerzo")
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuType.model_validate(menu_type),
            meal_time=sch_menu.MealTime.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


def get_all_meriendas(db: Session):
    menus = (
        db.query(mod_menu, mod_menu_type, mod_meal_time)
        .join(mod_menu_type, mod_menu.id_menu_type == mod_menu_type.id_menu_type)
        .join(mod_meal_time, mod_menu.id_meal_time == mod_meal_time.id_meal_time)
        .filter(mod_meal_time.meal_time == "Merienda")
        .all()
    )

    response = [
        sch_menu.MenuWithTypeTime(
            menu=sch_menu.MenuOut.model_validate(menu),
            menu_type=sch_menu.MenuType.model_validate(menu_type),
            meal_time=sch_menu.MealTime.model_validate(meal_time),
        )
        for menu, menu_type, meal_time in menus
    ]

    return response


def get_only_menu(db: Session, menu_id: int):
    menu = db.query(mod_menu).filter(mod_menu.id_menu == menu_id).first()

    return menu


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
    if db_menu is None:
        return None

    db.delete(db_menu)
    db.commit()
    return db_menu


def comprobrar_reservacion_menu(db: Session, menu_id: int):
    db_menu = (
        db.query(mod_menu)
        .join(mod_dining, mod_menu.id_menu == mod_dining.id_menu)
        .filter(mod_menu.id_menu == menu_id)
        .first()
    )
    if db_menu is None:
        return True
    return False


def get_meal_time(db: Session, meal_time_id: int):
    db_meal_time = (
        db.query(mod_meal_time)
        .filter(mod_meal_time.id_meal_time == meal_time_id)
        .first()
    )
    return db_meal_time
