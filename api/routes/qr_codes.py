from fastapi import HTTPException, APIRouter, Depends
from api.schemas import sch_dinings as sch_dining
from api.crud import crd_dinings as crd_dining
from datetime import date, time
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

    if reserva is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reserva.id_status == 2:
        raise HTTPException(status_code=403, detail="Reservation was cancelled time ago")
    
    if reserva.id_status == 3:
        raise HTTPException(status_code=403, detail="Reservation already used")
    
    is_valid = (
        reserva.id_reservation == data.id_reserva
        and reserva.reservation_date == data.fecha_reserva
        and reserva.reservation_hour == data.hora_reserva
    )

    print("COMPARATIVA\n\n\n")
    print(reserva.id_reservation, " --- ", data.id_reserva, " ", reserva.id_reservation == data.id_reserva)
    print(reserva.reservation_date , " --- ", data.fecha_reserva, " ", reserva.reservation_date == data.fecha_reserva)
    print(reserva.reservation_hour , " --- ", data.hora_reserva, " ", reserva.reservation_hour == data.hora_reserva)

    if is_valid:
        reserva = crd_dining.get_only_dining_reservation(db, data.id_reserva)
        reserva.id_status = 3

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

    return {"valid": is_valid}
