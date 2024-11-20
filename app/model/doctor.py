from pydantic import BaseModel

class Doctor(BaseModel):
    id: str
    name: str
    specialization: str
    workDays: list[str]
    phone: str
    start: str
    end: str
    rate: float
    image: str