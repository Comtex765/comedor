from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_dinings as sch_dining
from api.crud import crd_dinings as crd_dining
from sqlalchemy.orm import Session
from api.database import get_db
from typing import List

router = APIRouter()


@router.get("/reservations/", response_model=List[sch_dining.DiningReservationOut])
async def read_dining_reservations(db: Session = Depends(get_db)):
    reservations = crd_dining.get_dining_reservations(db)
    return reservations


@router.get(
    "/reservations/{reservation_id}", response_model=sch_dining.DiningReservationOut
)
async def read_dining_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = crd_dining.get_dining_reservation(db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.post("/reservations/", response_model=sch_dining.DiningReservationOut)
async def create_dining_reservation(
    reservation: sch_dining.DiningReservationCreate, db: Session = Depends(get_db)
):
    return crd_dining.create_dining_reservation(db, reservation=reservation)


@router.put(
    "/reservations/{reservation_id}", response_model=sch_dining.DiningReservationOut
)
async def update_dining_reservation(
    reservation_id: int,
    reservation: sch_dining.DiningReservationUpdate,
    db: Session = Depends(get_db),
):
    db_reservation = crd_dining.get_dining_reservation(
        db, reservation_id=reservation_id
    )
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return crd_dining.update_dining_reservation(
        db, reservation_id=reservation_id, reservation=reservation
    )


@router.delete(
    "/reservations/{reservation_id}", response_model=sch_dining.DiningReservationOut
)
async def delete_dining_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crd_dining.get_dining_reservation(
        db, reservation_id=reservation_id
    )
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return crd_dining.delete_dining_reservation(db, reservation_id=reservation_id)
