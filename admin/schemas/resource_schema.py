from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl, EmailStr


class HandicapType(str, Enum):
    MOTOR = "motor"
    VISUAL = "visual"
    AUDITORY = "auditory"


class ResourceBase(BaseModel):
    name: str
    resource_type: str
    description: Optional[str] = None

    handicap_type: Optional[HandicapType] = None

    region: Optional[str] = None
    city: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None


class ResourceCreate(ResourceBase):
    validated: bool = True


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    resource_type: Optional[str] = None
    description: Optional[str] = None

    handicap_type: Optional[HandicapType] = None

    region: Optional[str] = None
    city: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None

    validated: Optional[bool] = None


class ResourceOut(BaseModel):
    id: int
    name: str
    resource_type: str
    description: Optional[str]

    handicap_id: Optional[int]
    handicap_type: Optional[str]

    region: Optional[str]
    city: Optional[str]

    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]

    validated: bool
    created_at: datetime

    class Config:
        from_attributes = True
