from datetime import date, time, datetime, timedelta, timezone
from api.schemas import sch_dinings as sch_dining
from api.crud import crd_dinings as crd_dining
from api.crud import crd_menus as crd_menu
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from api.database import get_db
from pydantic import BaseModel


router = APIRouter()


class QRCodeData(BaseModel):
    nombre: str
    id_reserva: int
    menu: str
    hora_reserva: time
    fecha_reserva: date


@router.post("/validate_qr")
async def validate_qr(data: QRCodeData, db: Session = Depends(get_db)):
    reserva = crd_dining.get_only_dining_reservation(db, data.id_reserva)
    menu = crd_menu.get_only_menu(db, reserva.id_menu)
    meal_time = crd_menu.get_meal_time(db, menu.id_meal_time)

    if reserva is None:
        return {"valid": False, "detail": "No se encontró ninguna reserva asociada"}
    elif reserva.id_status == 2:
        return {"valid": False, "detail": "La reserva fue cancelada con anterioridad"}
    elif reserva.id_status == 3:
        return {"valid": False, "detail": "Ya fue utilizada la reserva"}

    is_valid = (
        reserva.id_reservation == data.id_reserva
        and reserva.reservation_date == data.fecha_reserva
        and reserva.reservation_hour == data.hora_reserva
    )

    current_hour = datetime.now(timezone.utc)
    current_hour_offset = timedelta(hours=-5)
    current_hour = current_hour + current_hour_offset
    current_hour = current_hour.strftime("%H:%M:%S")

    print(f"\n\nHORA ACTUAL --> {current_hour}")

    if current_hour < meal_time.init_hour.strftime("%H:%M:%S"):
        return {
            "valid": False,
            "detail": "Aún no es la hora de la comida de tu reserva",
        }
    if current_hour > meal_time.end_hour.strftime("%H:%M:%S"):
        return {
            "valid": False,
            "detail": "La hora de la comida de tu reserva ya pasó",
        }

    if is_valid:

        update(db, 3, data)
        return {"valid": True, "detail": "Reserva validada correctamente"}

    return {"valid": False, "detail": "La reserva NO es válida"}


def update(db: Session, status: int, data: QRCodeData):
    reserva = crd_dining.get_only_dining_reservation(db, data.id_reserva)
    reserva.id_status = status

    reservation_dict = {
        "id_menu": reserva.id_menu,
        "id_user": reserva.id_user,
        "id_status": reserva.id_status,
        "reservation_date": reserva.reservation_date,
        "reservation_hour": reserva.reservation_hour,
        "created_date": reserva.created_date,
        "total_cost": reserva.total_cost,
    }

    reservation_dict = sch_dining.DiningReservationUpdate(**reservation_dict)

    crd_dining.update_dining_reservation(
        db, reservation_id=reserva.id_reservation, reservation=reservation_dict
    )
