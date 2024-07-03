from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: str
    type: int


class UserToken(BaseModel):
    email: str
    type: int
