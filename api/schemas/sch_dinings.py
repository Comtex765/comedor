from api.schemas.sch_menus import MenuWithTypeTime
from api.schemas.sch_users import UserWithType
from datetime import date, time, datetime
from pydantic import BaseModel


class DiningReservationBase(BaseModel):
    id_menu: int
    id_user: int

    reservation_date: date
    reservation_hour: time


class DiningReservationCreate(DiningReservationBase):
    pass


class DiningReservationUpdate(DiningReservationBase):
    pass


class DiningReservationOut(DiningReservationBase):
    id_reservation: int
    id_status: int
    created_date: datetime
    total_cost: float

    class Config:
        from_attributes = True


class ReserveStatus(BaseModel):
    id_status: int
    reserve_status: str

    class Config:
        from_attributes = True


class ReservationWhole(BaseModel):
    reservation: DiningReservationOut
    user: UserWithType
    menu: MenuWithTypeTime
    reserveStatus: ReserveStatus
