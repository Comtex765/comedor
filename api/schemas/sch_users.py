from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id_user_type: int
    user_name: str
    user_last_name: str
    email: EmailStr
    cellphone: str
    cedula: str


class UserCreate(UserBase):
    hash_password: str


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id_user: int
    created_date: datetime
    balance: float

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
