from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    phone: str
    bloodType: str
    weight: int
    hight: int
    bmi: float
    age: int