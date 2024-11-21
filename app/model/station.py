from pydantic import BaseModel

class Station(BaseModel):
    name: str
    manager: str
    phone: str
    location: str
    
class StationU(BaseModel):
    id: int
    name: str
    manager: str
    phone: str
    location: str