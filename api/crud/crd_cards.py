from api.schemas import sch_cards as sch_card
from api.models import Card as mod_card
from sqlalchemy.orm import Session



def create_card(db: Session, card: sch_card.CardCreate):
    db_card = mod_card(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_card(db: Session, card_id: int):
    return db.query(mod_card).filter(mod_card.id_card == card_id).first()

def get_cards(db: Session):
    return db.query(mod_card).all()

def update_card(db: Session, card_id: int, card: sch_card.CardUpdate):
    db_card = db.query(mod_card).filter(mod_card.id_card == card_id).first()
    if db_card is None:
        return None
    for key, value in card.model_dump().items():
        setattr(db_card, key, value)
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, card_id: int):
    db_card = db.query(mod_card).filter(mod_card.id_card == card_id).first()
    if db_card is None:
        return None
    db.delete(db_card)
    db.commit()
    return db_card
