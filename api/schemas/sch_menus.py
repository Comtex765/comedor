from pydantic import BaseModel


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
