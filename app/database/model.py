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

from typing import List, Optional

class Admins(SQLModel, table=True):
    __tablename__ = "admins"
    id: int = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True)
    password: str


class Stations(SQLModel, table=True):
    __tablename__ = "stations"
    id: int = Field(default=None, primary_key=True)
    name: str
    phone: str
    location: str
    
    admin_id: Optional[int] = Field(default=None, foreign_key="admins.id", nullable=False)
    
    # Relationship with Admins model
    admin: Optional["Admins"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"})
