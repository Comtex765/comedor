from api.crud.crd_menus import convert_menu_to_menu_with_time_type
from api.crud.crd_users import convert_user_to_user_with_type
from api.models import DiningReservation as mod_reservation
from api.models import ReserveStatus as mod_reserve_status
from api.models import DiningReservation as mod_dining
from api.schemas import sch_dinings as sch_dinings
from api.crud import crd_menus as crd_menu
from api.crud import crd_users as crd_user
from sqlalchemy.orm import Session
from datetime import datetime


def get_dining_reservation_by_id(db: Session, reservation_id: int):
    reservations = (
        db.query(mod_reservation)
        .join(
            mod_reserve_status,
            mod_reservation.id_status == mod_reserve_status.id_status,
        )
        .filter(mod_reservation.id_reservation == reservation_id)
        .all()
    )

    result = []

    for res in reservations:
        # Obtener información de usuario y menú para esta reserva
        user_info = convert_user_to_user_with_type(res.user)
        menu_info = convert_menu_to_menu_with_time_type(res.menu)

        # Crear un diccionario con la información combinada
        reservation_data = {
            "reservation": {
                "id_reservation": res.id_reservation,
                "id_menu": res.id_menu,
                "id_user": res.id_user,
                "id_status": res.id_status,
                "reservation_date": res.reservation_date,
                "reservation_hour": res.reservation_hour,
                "created_date": res.created_date,
                "total_cost": res.total_cost,
            },
            "user": user_info.model_dump(),
            "menu": menu_info.model_dump(),
            "reserveStatus": {
                "id_status": res.reserve_status.id_status,
                "reserve_status": res.reserve_status.reserve_status,
            },
        }

        result.append(reservation_data)

    return result[0]


def get_dining_reservations(db: Session):
    reservations = (
        db.query(mod_reservation)
        .join(
            mod_reserve_status,
            mod_reservation.id_status == mod_reserve_status.id_status,
        )
        .all()
    )

    result = []

    for res in reservations:
        # Obtener información de usuario y menú para esta reserva
        user_info = convert_user_to_user_with_type(res.user)
        menu_info = convert_menu_to_menu_with_time_type(res.menu)

        # Crear un diccionario con la información combinada
        reservation_data = {
            "reservation": {
                "id_reservation": res.id_reservation,
                "id_menu": res.id_menu,
                "id_user": res.id_user,
                "id_status": res.id_status,
                "reservation_date": res.reservation_date,
                "reservation_hour": res.reservation_hour,
                "created_date": res.created_date,
                "total_cost": res.total_cost,
            },
            "user": user_info.model_dump(),
            "menu": menu_info.model_dump(),
            "reserveStatus": {
                "id_status": res.reserve_status.id_status,
                "reserve_status": res.reserve_status.reserve_status,
            },
        }

        result.append(reservation_data)

    return result


""" 
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
 """


def create_dining_reservation(
    db: Session, reservation: sch_dinings.DiningReservationCreate
):
    db_reservation = mod_dining(**reservation.model_dump())
    db_reservation.id_status = 1
    db_reservation.created_date = datetime.now()

    price = crd_menu.get_menu_price(db=db, menu_id=db_reservation.id_menu)
    discount = crd_user.get_user_discount(db=db, user_id=db_reservation.id_user)

    db_reservation.total_cost = float(price) * (100 - discount) / 100

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation


def update_dining_reservation(
    db: Session, reservation_id: int, reservation: sch_dinings.DiningReservationUpdate
):
    db_reservation = (
        db.query(mod_dining).filter(mod_dining.id_reservation == reservation_id).first()
    )
    if db_reservation:
        for key, value in reservation.model_dump(exclude_unset=True).items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation


def delete_dining_reservation(db: Session, reservation_id: int):
    db_reservation = (
        db.query(mod_dining).filter(mod_dining.id_reservation == reservation_id).first()
    )
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation
