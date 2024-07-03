from api.schemas import sch_cards as sch_card
from api.models import Card as mod_card
from sqlalchemy.orm import Session


def create_card(db: Session, card: sch_card.CardCreate):
    db_card = mod_card(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_card_by_card_id(db: Session, card_id: int):
    return db.query(mod_card).filter(mod_card.id_card == card_id).first()


def get_card_by_user_id(db: Session, user_id: int):
    return db.query(mod_card).filter(mod_card.id_user == user_id).first()


def get_cards(db: Session):
    return db.query(mod_card).all()


def update_card(db: Session, card_id: int, card: sch_card.CardUpdate):
    db_card = db.query(mod_card).filter(mod_card.id_card == card_id).first()

    if db_card:
        for field, value in card.model_dump(exclude_unset=True).items():
            setattr(db_card, field, value)

        db.commit()
        db.refresh(db_card)

        return db_card

    return None


def delete_card(db: Session, card_id: int):
    db_card = db.query(mod_card).filter(mod_card.id_card == card_id).first()
    if db_card is None:
        return None
    db.delete(db_card)
    db.commit()
    return db_card
