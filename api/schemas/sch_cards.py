from pydantic import BaseModel
from typing import Optional


class CardBase(BaseModel):
    card_number: str
    exp_month: str
    exp_year: str
    id_user: Optional[int]


class CardCreate(CardBase):
    pass


class CardUpdate(CardBase):
    pass


class CardOut(CardBase):
    id_card: int

    class Config:
        from_attributes = True
