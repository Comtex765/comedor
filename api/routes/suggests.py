from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_suggests as sch_suggest
from api.crud import crd_suggests as crd_suggest
from sqlalchemy.orm import Session
from api.database import get_db
from typing import List


router = APIRouter()


@router.post("", response_model=sch_suggest.SuggestOut)
def create_suggestion(
    suggest: sch_suggest.SuggestCreate, db: Session = Depends(get_db)
):
    suggest.suggestion
    return crd_suggest.create_suggest(db=db, suggest=suggest)


@router.get("", response_model=List[sch_suggest.SuggestOut])
def read_suggestions(db: Session = Depends(get_db)):
    return crd_suggest.get_suggests(db=db)


@router.get("/{suggest_id}", response_model=sch_suggest.SuggestOut)
def read_suggestion(suggest_id: int, db: Session = Depends(get_db)):
    db_suggest = crd_suggest.get_suggest(db=db, suggest_id=suggest_id)
    if db_suggest is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return db_suggest


@router.put("/{suggest_id}", response_model=sch_suggest.SuggestOut)
def update_suggestion(
    suggest_id: int, suggest: sch_suggest.SuggestUpdate, db: Session = Depends(get_db)
):
    db_suggest = crd_suggest.update_suggest(
        db=db, suggest_id=suggest_id, suggest_update=suggest
    )
    if db_suggest is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return db_suggest


@router.delete("/{suggest_id}", response_model=sch_suggest.SuggestOut)
def delete_suggestion(suggest_id: int, db: Session = Depends(get_db)):
    db_suggest = crd_suggest.delete_suggest(db=db, suggest_id=suggest_id)
    if db_suggest is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return db_suggest
