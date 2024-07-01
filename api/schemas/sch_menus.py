from pydantic import BaseModel
from datetime import time


class MenuBase(BaseModel):
    id_menu_type: int
    id_meal_time: int
    menu_title: str
    menu_description: str
    price: float


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuOut(MenuBase):
    id_menu: int
    status: bool

    class Config:
        from_attributes = True


class MealTimeBase(BaseModel):
    id_meal_time: int
    meal_time: str
    init_hour: time
    end_hour: time

    class Config:
        from_attributes = True


class MenuTypeBase(BaseModel):
    id_menu_type: int
    menu_type: str

    class Config:
        from_attributes = True


class MenuWithTypeTime(BaseModel):
    menu: MenuOut
    menu_type: MenuTypeBase
    meal_time: MealTimeBase
