from api.schemas.sch_menus import MenuWithTypeTime
from api.schemas.sch_users import UserWithType
from datetime import date, time, datetime
from pydantic import BaseModel, field_validator


class DiningReservationBase(BaseModel):
    id_menu: int
    id_user: int

    reservation_date: date
    reservation_hour: time

    @field_validator("reservation_hour")
    def format_reservation_hour(cls, value):
        # Asegurar que los segundos siempre sean 00
        formatted_value = value.replace(second=0, microsecond=0)
        return formatted_value


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
