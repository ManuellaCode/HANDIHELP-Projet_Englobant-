from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


class HandicapType(str, Enum):
    MOTOR = "motor"
    VISUAL = "visual"
    AUDITORY = "auditory"


class SolutionCreate(BaseModel):
    title: str
    category: str
    handicap_type: Optional[HandicapType] = None

    age_min: Optional[int] = None
    age_max: Optional[int] = None

    content: str
    source_url: Optional[HttpUrl] = None
    tags: Optional[str] = None

    published: bool = False


class SolutionUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    handicap_type: Optional[HandicapType] = None

    age_min: Optional[int] = None
    age_max: Optional[int] = None

    content: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    tags: Optional[str] = None

    published: Optional[bool] = None


class SolutionOut(BaseModel):
    id: int
    title: str
    category: str

    handicap_id: Optional[int] = None
    handicap_type: Optional[str] = None  # on le remplira via handicap.name

    age_min: Optional[int] = None
    age_max: Optional[int] = None

    content: str
    source_url: Optional[str] = None
    tags: Optional[str] = None

    published: bool
    created_at: datetime

    class Config:
        from_attributes = True