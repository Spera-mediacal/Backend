from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    bloodType: str
    weight: int
    hight: int
    age: int