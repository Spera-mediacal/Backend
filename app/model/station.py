from pydantic import BaseModel

class Station(BaseModel):
    name: str
    manager: str
    phone: str
    location: str