from pydantic import BaseModel, EmailStr
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

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    balance: float


class UserOut(UserBase):
    id_user: int
    balance: float
    created_date: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SetBalance(BaseModel):
    email: EmailStr
    new_balance: float


class UserType(BaseModel):
    id_user_type: int
    description: str
    percent_discount: int

    class Config:
        from_attributes = True


class UserWithType(BaseModel):
    user: UserOut
    type: UserType
