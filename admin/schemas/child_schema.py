from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChildCreate(BaseModel):
    name: str
    age: int
    handicap_id: int
    parent_id: int


class ChildOut(BaseModel):
    id: int
    name: str
    age: int
    handicap_id: int
    parent_id: int
    created_at: datetime

    class Config:
        from_attributes = True