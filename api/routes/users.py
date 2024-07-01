from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_users as sch_user
from api.crud import crd_users as crd_user
from api.crud import crd_cards as crd_card
from api.utils.cedula import check_cedula
from sqlalchemy.orm import Session
from api.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=sch_user.UserOut)
async def create_user(user: sch_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crd_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crd_user.get_user_cellphone(db, cell=user.cellphone)
    if db_user:
        raise HTTPException(status_code=400, detail="Cellphone already registered")

    db_user = crd_user.get_user_cedula(db, ced=user.cedula)
    if db_user:
        raise HTTPException(status_code=400, detail="Cedula already registered")

    if check_cedula(user.cedula) is False:
        raise HTTPException(status_code=400, detail="Cedula is invalid")
    return crd_user.create_user(db=db, user=user)


@router.post("/balance")
async def set_balance(balance: sch_user.SetBalance, db: Session = Depends(get_db)):
    user = crd_user.get_user_by_email(db, email=balance.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    card = crd_card.get_card_by_user_id(
        db, user_id=crd_user.get_user_id_by_email(db, email=balance.email)
    )
    if card is None:
        raise HTTPException(status_code=404, detail="User has not a card asscociated")

    db_user = crd_user.update_balance(
        db, user_id=user.id_user, balance=balance.new_balance
    )
    return db_user


@router.get("/id/{user_id}", response_model=sch_user.UserWithType)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crd_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/email/{user_email}", response_model=sch_user.UserWithType)
async def read_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crd_user.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[sch_user.UserWithType])
async def read_users(db: Session = Depends(get_db)):
    users = crd_user.get_users(db)
    return users


@router.put("/{user_id}", response_model=sch_user.UserOut)
async def update_user(
    user_id: int, user: sch_user.UserUpdate, db: Session = Depends(get_db)
):
    db_user = crd_user.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=sch_user.UserOut)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crd_user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
