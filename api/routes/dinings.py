from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_dinings as sch_dining
from api.schemas import sch_tokens as sch_token
from api.crud import crd_dinings as crd_dining
from api.utils.auth import get_current_user
from sqlalchemy.orm import Session

from api.database import get_db
from typing import List

router = APIRouter()


@router.get("", response_model=List[sch_dining.ReservationWhole])
async def read_dining_reservations(
    db: Session = Depends(get_db),
    current_user: sch_token.UserToken = Depends(get_current_user),
):
    if current_user.id_user_type == 0:
        reservations = crd_dining.get_dining_reservations(db)

        if reservations is None:
            raise HTTPException(status_code=404, detail="[]")
        return reservations
    else:
        return {"WAIT!": "You should'nt be here"}


@router.get("/{reservation_id}", response_model=sch_dining.ReservationWhole)
async def read_dining_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = crd_dining.get_dining_reservation_by_id(
        db, reservation_id=reservation_id
    )
    if reservation is None:
        raise HTTPException(status_code=404, detail="[]")
    return reservation


@router.get("/reportes/email/{email}", response_model=List[sch_dining.ReservationWhole])
async def read_dining_reservation(email: str, db: Session = Depends(get_db)):
    reservations = crd_dining.get_dinings_reservations_by_email(db=db, email=email)
    if reservations is None:
        raise HTTPException(status_code=404, detail="[]")
    return reservations


@router.post("", response_model=sch_dining.DiningReservationOut)
async def create_dining_reservation(
    reservation: sch_dining.DiningReservationCreate, db: Session = Depends(get_db)
):
    db_dining = crd_dining.create_dining_reservation(db, reservation=reservation)

    if db_dining is None:
        raise HTTPException(status_code=404, detail="Saldo insuficiente")
    return db_dining


@router.put("/{reservation_id}", response_model=sch_dining.DiningReservationOut)
async def update_dining_reservation(
    reservation_id: int,
    reservation: sch_dining.DiningReservationUpdate,
    db: Session = Depends(get_db),
):
    db_reservation = crd_dining.get_dining_reservation_by_id(
        db, reservation_id=reservation_id
    )

    if db_reservation is None:
        raise HTTPException(status_code=404, detail="[]")

    return crd_dining.update_dining_reservation(
        db, reservation_id=reservation_id, reservation=reservation
    )


@router.delete("/{reservation_id}", response_model=sch_dining.DiningReservationOut)
async def delete_dining_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crd_dining.delete_dining_reservation(
        db, reservation_id=reservation_id
    )
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_reservation
