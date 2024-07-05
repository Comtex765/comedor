from sqlalchemy import (
    Column,
    Text,
    Date,
    Integer,
    String,
    ForeignKey,
    Time,
    DECIMAL,
    TIMESTAMP,
    CHAR,
    BOOLEAN,
)
from sqlalchemy.orm import relationship, declarative_base

import bcrypt

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    id_user_type = Column(Integer, ForeignKey("user_type.id_user_type"))
    user_name = Column(String(100))
    user_last_name = Column(String(100))
    cedula = Column(CHAR(10), unique=True)
    email = Column(String(100), unique=True)
    hash_password = Column(String(200))
    cellphone = Column(CHAR(10), unique=True)
    balance = Column(DECIMAL(10, 2))
    created_date = Column(TIMESTAMP)

    user_type = relationship("UserType", back_populates="users")
    card = relationship("Card", uselist=False, back_populates="user")
    dining_reservations = relationship("DiningReservation", back_populates="user")
    codes = relationship("Code", back_populates="user")

    def set_password(self, password):
        self.hash_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hash_password.encode("utf-8")
        )


class UserType(Base):
    __tablename__ = "user_type"

    id_user_type = Column(Integer, primary_key=True)
    description = Column(String(100))
    percent_discount = Column(Integer)

    users = relationship("User", back_populates="user_type")


class Card(Base):
    __tablename__ = "card"

    id_card = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    card_number = Column(String(100), nullable=False)
    exp_month = Column(String(100), nullable=False)
    exp_year = Column(String(100), nullable=False)

    user = relationship("User", back_populates="card")


class Suggest(Base):
    __tablename__ = "suggests"

    id_suggest = Column(Integer, primary_key=True)
    suggestion = Column(Text)
    created_date = Column(TIMESTAMP)


class DiningReservation(Base):
    __tablename__ = "dining_reservation"

    id_reservation = Column(Integer, primary_key=True)
    id_menu = Column(Integer, ForeignKey("menu.id_menu"))
    id_user = Column(Integer, ForeignKey("users.id_user"))
    id_status = Column(Integer, ForeignKey("reserve_status.id_status"))
    reservation_date = Column(Date)
    reservation_hour = Column(Time)
    created_date = Column(TIMESTAMP)
    total_cost = Column(DECIMAL(5, 2))

    menu = relationship("Menu", back_populates="dining_reservations")
    user = relationship("User", back_populates="dining_reservations")
    reserve_status = relationship("ReserveStatus", back_populates="dining_reservations")


class ReserveStatus(Base):
    __tablename__ = "reserve_status"

    id_status = Column(Integer, primary_key=True)
    reserve_status = Column(String(50))

    dining_reservations = relationship(
        "DiningReservation", back_populates="reserve_status"
    )


class MenuType(Base):
    __tablename__ = "menu_type"

    id_menu_type = Column(Integer, primary_key=True)
    menu_type = Column(String(50))

    menus = relationship("Menu", back_populates="menu_type")


class MealTime(Base):
    __tablename__ = "meal_time"

    id_meal_time = Column(Integer, primary_key=True)
    meal_time = Column(String(50))
    init_hour = Column(Time)
    end_hour = Column(Time)

    menus = relationship("Menu", back_populates="meal_time")


class Menu(Base):
    __tablename__ = "menu"

    id_menu = Column(Integer, primary_key=True)
    id_menu_type = Column(Integer, ForeignKey("menu_type.id_menu_type"))
    id_meal_time = Column(Integer, ForeignKey("meal_time.id_meal_time"))
    menu_title = Column(String(50))
    menu_description = Column(Text)
    status = Column(BOOLEAN)
    price = Column(DECIMAL(5, 2))

    menu_type = relationship("MenuType", back_populates="menus")
    meal_time = relationship("MealTime", back_populates="menus")
    dining_reservations = relationship("DiningReservation", back_populates="menu")


class Code(Base):
    __tablename__ = "code"

    code = Column(String(6), primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    estado = Column(BOOLEAN)

    user = relationship("User", back_populates="codes")
