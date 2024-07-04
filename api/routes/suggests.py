from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_suggests as sch_suggest
from api.crud import crd_suggests as crd_suggest
from api.schemas import sch_tokens as sch_token
from api.utils.auth import get_current_user
from sqlalchemy.orm import Session

from api.database import get_db
from typing import List


router = APIRouter()


@router.post("", response_model=sch_suggest.SuggestOut)
def create_suggestion(
    suggest: sch_suggest.SuggestCreate, db: Session = Depends(get_db)
):
    return crd_suggest.create_suggest(db=db, suggest=suggest)


@router.get("", response_model=List[sch_suggest.SuggestOut])
def read_suggestions(
    db: Session = Depends(get_db),
    current_user: sch_token.UserToken = Depends(get_current_user),
):
    if current_user.id_user_type == 0:
        suggests = crd_suggest.get_suggests(db=db)
        if suggests is None:
            raise HTTPException(status_code=404, detail="[]")

        return suggests
    else:
        return {"WAIT!": "You should'nt be here"}


@router.get("/{suggest_id}", response_model=sch_suggest.SuggestOut)
def read_suggestion(suggest_id: int, db: Session = Depends(get_db)):
    db_suggest = crd_suggest.get_suggest(db=db, suggest_id=suggest_id)
    if db_suggest is None:
        raise HTTPException(status_code=404, detail="[]")
    return db_suggest
