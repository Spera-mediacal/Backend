from pydantic import BaseModel
from datetime import datetime

fullDate = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"

class Donate(BaseModel):
    id: str
    quantity: int
    date: str = fullDate