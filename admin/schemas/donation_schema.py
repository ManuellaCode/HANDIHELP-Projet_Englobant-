from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class DonationCreate(BaseModel):
    amount: float
    message: Optional[str] = None

    user_id: Optional[int] = None

    donor_name: Optional[str] = None
    donor_email: Optional[EmailStr] = None


class DonationOut(BaseModel):
    id: int
    amount: float
    message: Optional[str] = None

    user_id: Optional[int] = None
    donor_name: Optional[str] = None
    donor_email: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True


class DonationStats(BaseModel):
    total_donations: int
    total_amount: float
    average_donation: float