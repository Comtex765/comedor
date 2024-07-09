from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_tokens as sch_token
from api.schemas import sch_cards as sch_card
from api.utils.auth import get_current_user
from api.crud import crd_cards as crd_card
from api.crud import crd_users as crd_user
from sqlalchemy.orm import Session

from api.database import get_db

router = APIRouter()


@router.post("", response_model=sch_card.CardOut)
async def create_card(card: sch_card.CardCreate, db: Session = Depends(get_db)):
    db_card = crd_card.get_card_by_user_id(db, user_id=card.id_user)

    if db_card:
        raise HTTPException(
            status_code=404, detail="El usuario ya tiene una tarjeta asociada"
        )

    user = crd_user.get_user_by_id(db, user_id=card.id_user)
    if user is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return crd_card.create_card(db=db, card=card)


@router.get("/{card_id}", response_model=sch_card.CardOut)
async def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crd_card.get_card_by_card_id(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_card


@router.get("/user_id/{user_id}", response_model=sch_card.CardOut)
async def read_card(user_id: int, db: Session = Depends(get_db)):
    db_card = crd_card.get_card_by_user_id(db, user_id=user_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_card


@router.get("", response_model=list[sch_card.CardOut])
async def read_cards(
    db: Session = Depends(get_db),
    current_user: sch_token.UserToken = Depends(get_current_user),
):
    if current_user.id_user_type == 0:
        cards = crd_card.get_cards(db)
        return cards
    else:
        return {"WAIT!": "You should'nt be here"}


@router.put("/{card_id}", response_model=sch_card.CardOut)
async def update_card(
    card_id: int, card: sch_card.CardUpdate, db: Session = Depends(get_db)
):
    db_card = crd_card.update_card(db, card_id=card_id, card=card)
    if db_card is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_card


@router.delete("/{card_id}", response_model=sch_card.CardOut)
async def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crd_card.delete_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_card
