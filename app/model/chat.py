from pydantic import BaseModel

class RequestModel(BaseModel):
    msg: str