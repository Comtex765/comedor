from pydantic import BaseModel
from datetime import datetime


class SuggestBase(BaseModel):
    suggestion: str


class SuggestCreate(SuggestBase):
    pass


class SuggestUpdate(SuggestBase):
    pass


class SuggestOut(SuggestBase):
    id_suggest: int
    created_date: datetime

    class Config:
        from_attributes = True
