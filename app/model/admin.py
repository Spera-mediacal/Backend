from pydantic import BaseModel

class Admin(BaseModel):
    name: str
    username: str
    password: str