from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: Optional[str] = None
