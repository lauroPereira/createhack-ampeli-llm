from pydantic import BaseModel

class Group(BaseModel):
    name: str
    description: str
    leader_phone: str

class Ministry(BaseModel):
    name: str
    description: str
    leader_phone: str

class Cell(BaseModel):
    name: str
    description: str
    leader_phone: str
