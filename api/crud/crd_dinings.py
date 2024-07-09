from api.crud.crd_menus import convert_menu_to_menu_with_time_type
from api.crud.crd_users import convert_user_to_user_with_type
from api.models import DiningReservation as mod_reservation
from api.models import ReserveStatus as mod_reserve_status
from api.models import DiningReservation as mod_dining
from api.email.reservation_ticket import send_email
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

    if reservations:
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
    return None


def get_dinings_reservations_by_email(db: Session, email: str):
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

        if reservation_data["user"]["user"]["email"] == email:
            result.append(reservation_data)

    return result


def get_only_dining_reservation(db: Session, reservation_id: int):
    reservation = (
        db.query(mod_reservation)
        .filter(mod_reservation.id_reservation == reservation_id)
        .first()
    )
    if reservation:
        return reservation
    return None


def create_dining_reservation(
    db: Session, reservation: sch_dinings.DiningReservationCreate
):
    db_reservation = mod_dining(**reservation.model_dump())
    db_reservation.id_status = 1
    db_reservation.created_date = datetime.now()

    price = crd_menu.get_menu_price(db=db, menu_id=db_reservation.id_menu)
    discount = crd_user.get_user_discount(db=db, user_id=db_reservation.id_user)

    db_reservation.total_cost = float(price) * (100 - discount) / 100

    user_balance = float(
        crd_user.get_only_balance_by_id(db=db, user_id=reservation.id_user)
    )

    if user_balance >= db_reservation.total_cost:
        db_reservation.reservation_hour = db_reservation.reservation_hour.strftime(
            "%H:%M:%S"
        )

        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)

        crd_user.update_balance(
            db=db, user_id=reservation.id_user, balance=(-1 * db_reservation.total_cost)
        )

        send_email(
            get_dining_reservation_by_id(
                db=db, reservation_id=db_reservation.id_reservation
            )
        )

        return db_reservation
    else:
        return None


def update_dining_reservation(
    db: Session,
    reservation_id: int,
    reservation: sch_dinings.DiningReservationUpdate,
):
    db_reservation = (
        db.query(mod_dining).filter(mod_dining.id_reservation == reservation_id).first()
    )
    if db_reservation:
        for field, value in reservation.model_dump(exclude_unset=True).items():
            setattr(db_reservation, field, value)

        db.commit()
        db.refresh(db_reservation)

        return db_reservation

    return None


def delete_dining_reservation(db: Session, reservation_id: int):
    db_reservation = (
        db.query(mod_dining).filter(mod_dining.id_reservation == reservation_id).first()
    )
    if db_reservation is None:
        return None

    db.delete(db_reservation)
    db.commit()
    return db_reservation
