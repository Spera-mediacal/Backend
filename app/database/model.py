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
    bmi: float
    lastdonate: str

class DonationHistory(SQLModel, table=True):
    __tablename__ = "donations_history"
    id: int = Field(default=None, primary_key=True)
    quantity: int
    date: str
    user_id: str = Field(foreign_key="users.id", nullable=False)
    user: UserTB | None = Relationship(sa_relationship_kwargs={"cascade": "all, delete"})

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
    address: str
    joinDate: str
    image: str
    
class Stations(SQLModel, table=True):
    __tablename__ = "stations"
    id: int = Field(default=None, primary_key=True)
    name: str
    admin_id: int = Field(foreign_key="admin.id")
    admin: Optional["Admins"] = Relationship(back_populates="stations")
    phone: str
    location: str

class Admins(SQLModel, table=True):
    __tablename__ = "admin"
    id: int = Field(default=None, primary_key=True)
    name: str
    username: str
    password: str
    station_id: list = Field(foreign_key="stations.id")
    stations = List[Stations] = Relationship(back_populates="admin")