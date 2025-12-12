from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.don import Donation
from .base import BaseRepository


class DonationRepository(BaseRepository[Donation]):
    def __init__(self, db: Session):
        super().__init__(db, Donation)

    def list_latest(self, skip: int = 0, limit: int = 100) -> list[Donation]:
        return (
            self.db.query(Donation)
            .order_by(Donation.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def total_amount(self) -> float:
        total = self.db.query(func.sum(Donation.amount)).scalar()
        return float(total or 0.0)

    def stats(self) -> dict[str, float]:
        total_donations = self.db.query(func.count(Donation.id)).scalar() or 0
        total_amount = self.db.query(func.sum(Donation.amount)).scalar() or 0.0
        avg = (total_amount / total_donations) if total_donations else 0.0
        return {
            "total_donations": float(total_donations),
            "total_amount": float(total_amount),
            "average_donation": float(avg),
        }