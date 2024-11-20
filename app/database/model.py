from sqlmodel import SQLModel, Field, Relationship

class UserTB(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default=None, primary_key=True)
    name: str
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