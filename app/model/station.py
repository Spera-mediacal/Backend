from pydantic import BaseModel

class Station(BaseModel):
    name: str
    admin_id: int
    phone: str
    location: str
    
class StationU(BaseModel):
    id: int
    name: str
    admin_id: int
    phone: str
    location: str