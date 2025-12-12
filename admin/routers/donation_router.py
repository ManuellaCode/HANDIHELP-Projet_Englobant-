from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.donation_schema import DonationCreate, DonationOut, DonationStats
from ..services.donation_service import (
    create_donation,
    get_donation_stats,
    get_total_donations,
    list_donations,
)

router = APIRouter(prefix="/admin/donations", tags=["Donation Management"])


@router.post("/", response_model=DonationOut, status_code=status.HTTP_201_CREATED)
def create(payload: DonationCreate, db: Session = Depends(get_db)):
    return create_donation(db, payload)


@router.get("/", response_model=list[DonationOut])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_donations(db, skip=skip, limit=limit)


@router.get("/total")
def get_total(db: Session = Depends(get_db)):
    return get_total_donations(db)


@router.get("/stats", response_model=DonationStats)
def stats(db: Session = Depends(get_db)):
    return get_donation_stats(db)