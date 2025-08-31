from pydantic import BaseModel
from typing import List
from .member import Member
from .groups import Group, Ministry, Cell

class RecommendationItem(BaseModel):
    name: str
    description: str
    score: float

class ConnectionRequest(BaseModel):
    member: Member
    groups: List[Group]
    ministries: List[Ministry]
    cells: List[Cell]

class ConnectionResponse(BaseModel):
    groups: List[RecommendationItem]
    ministries: List[RecommendationItem]
    cells: List[RecommendationItem]
