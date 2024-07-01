from api.schemas import sch_suggests as sch_suggest
from api.models import Suggest as mod_suggest
from sqlalchemy.orm import Session
from datetime import datetime


def create_suggest(db: Session, suggest: sch_suggest.SuggestCreate):
    db_suggest = mod_suggest(
        suggestion=suggest.suggestion,
        created_date=datetime.now(),
    )
    db.add(db_suggest)
    db.commit()
    db.refresh(db_suggest)
    return db_suggest


def get_suggests(db: Session):
    return db.query(mod_suggest).all()


def get_suggest(db: Session, suggest_id: int):
    return db.query(mod_suggest).filter(mod_suggest.id_suggest == suggest_id).first()


def update_suggest(
    db: Session, suggest_id: int, suggest_update: sch_suggest.SuggestUpdate
):
    db_suggest = (
        db.query(mod_suggest).filter(mod_suggest.id_suggest == suggest_id).first()
    )
    if not db_suggest:
        return None
    for key, value in suggest_update.dict(exclude_unset=True).items():
        setattr(db_suggest, key, value)
    db.commit()
    db.refresh(db_suggest)
    return db_suggest


def delete_suggest(db: Session, suggest_id: int):
    db_suggest = (
        db.query(mod_suggest).filter(mod_suggest.id_suggest == suggest_id).first()
    )
    if not db_suggest:
        return None
    db.delete(db_suggest)
    db.commit()
    return db_suggest
