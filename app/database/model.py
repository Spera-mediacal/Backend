from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.types import JSON
from typing import List, Optional

class UserTB(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default=None, primary_key=True)
    name: str
    phone: str
    bloodType: str
    weight: int
    hight: int
    age: int
    lastdonate: str

class DonationHistory(SQLModel, table=True):
    __tablename__ = "donations_history"
    id: int = Field(default=None, primary_key=True)
    quantity: int
    date: str
    user_id: str = Field(foreign_key="users.id")
    user: UserTB | None = Relationship()

class Doctors(SQLModel, table=True):
    __tablename__ = "doctors"
    id: str = Field(default=None, primary_key=True)
    name: str
    specialization: str
    workDays: Optional[List[str]] = Field(default=None, sa_type=JSON)
    phone: str
    start: str
    end: str
    rate: float
    image: str