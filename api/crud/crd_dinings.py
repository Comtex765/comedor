from api.models import DiningReservation as mod_dining
from api.schemas import sch_dinings as sch_dinings
from api.crud import crd_menus as crd_menu
from api.crud import crd_users as crd_user
from sqlalchemy.orm import Session
from datetime import datetime


def get_dining_reservation(db: Session, reservation_id: int):
    return (
        db.query(mod_dining).filter(mod_dining.id_reservation == reservation_id).first()
    )


def get_dining_reservations(db: Session):
    return db.query(mod_dining).all()


def create_dining_reservation(
    db: Session, reservation: sch_dinings.DiningReservationCreate
):
    db_reservation = mod_dining(**reservation.model_dump())
    db_reservation.id_status = 1
    db_reservation.created_date = datetime.now()

    menu = crd_menu.get_menu_by_id(db=db, menu_id=db_reservation.id_menu)
    discount = crd_user.get_user_discount(db=db, user_id=db_reservation.id_user)

    db_reservation.total_cost = menu.price * (100 - discount) / 100

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
