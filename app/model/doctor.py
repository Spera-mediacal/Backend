from pydantic import BaseModel
from datetime import datetime

fullDate = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"

class Doctor(BaseModel):
    id: str
    name: str
    specialization: str
    workDays: list[str]
    phone: str
    start: str
    end: str
    rate: float
    address: str
    joinDate: str = fullDate
    image: str