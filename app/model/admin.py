from pydantic import BaseModel

class Admin(BaseModel):
    id: int
    name: str
    username: str
    password: str