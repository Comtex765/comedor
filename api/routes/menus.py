from fastapi import APIRouter, Depends, HTTPException
from api.schemas import sch_menus as sch_menu
from api.crud import crd_menus as crd_menu
from sqlalchemy.orm import Session
from api.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=sch_menu.MenuOut)
async def create_menu(menu: sch_menu.MenuCreate, db: Session = Depends(get_db)):
    return crd_menu.create_menu(db=db, menu=menu)


@router.get("/{menu_id}", response_model=sch_menu.MenuOut)
async def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crd_menu.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu


@router.get("/", response_model=List[sch_menu.MenuOut])
async def read_menus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    menus = crd_menu.get_menus(db=db, skip=skip, limit=limit)
    return menus


@router.put("/{menu_id}", response_model=sch_menu.MenuOut)
async def update_menu(
    menu_id: int, menu: sch_menu.MenuUpdate, db: Session = Depends(get_db)
):
    db_menu = crd_menu.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return crd_menu.update_menu(db=db, menu_id=menu_id, menu=menu)


@router.delete("/{menu_id}", response_model=sch_menu.MenuOut)
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crd_menu.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return crd_menu.delete_menu(db=db, menu_id=menu_id)
