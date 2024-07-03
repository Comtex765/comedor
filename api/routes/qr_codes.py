from api.crud import crd_dinings as crd_dining
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.database import get_db

router = APIRouter()


class QRCodeData(BaseModel):
    nombre: str
    id_reserva: int
    menu: str
    hora_reserva: str
    fecha_reserva: str


@router.post("/validate_qr")
async def validate_qr(data: QRCodeData, db: Session = Depends(get_db)):
    reserva = crd_dining.get_only_dining_reservation(db, data.id_reserva)

    is_valid = (
        reserva.id_reservation == data.id_reserva
        and reserva.reservation_date == data.fecha_reserva
        and reserva.reservation_hour == data.hora_reserva
    )

    reserva = crd_dining.get_only_dining_reservation(db, data.id_reserva)
    reserva.id_status = 3

    crd_dining.update_dining_reservation(
        db, reservation_id=reserva.id_reservation, reservation=reserva
    )

    return {"valid": is_valid}
