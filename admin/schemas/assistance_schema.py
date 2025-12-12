from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AssistanceRequestOut(BaseModel):
    id: int
    user_id: int
    category: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str  # "pending" | "approved" | "rejected"