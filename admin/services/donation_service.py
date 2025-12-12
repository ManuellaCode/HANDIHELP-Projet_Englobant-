from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.don import Donation
from ..repository.donation_repository import DonationRepository
from ..repository.user_repository import UserRepository
from ..schemas.donation_schema import DonationCreate


def create_donation(db: Session, payload: DonationCreate) -> Donation:
    donation_repo = DonationRepository(db)

    if payload.user_id is not None:
        user_repo = UserRepository(db)
        user = user_repo.get(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        donation = Donation(
            user_id=payload.user_id,
            amount=payload.amount,
            message=payload.message,
            donor_name=None,
            donor_email=None,
        )
        return donation_repo.create(donation)

    donation = Donation(
        user_id=None,
        amount=payload.amount,
        message=payload.message,
        donor_name=payload.donor_name,
        donor_email=str(payload.donor_email) if payload.donor_email else None,
    )
    return donation_repo.create(donation)

def list_donations(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les donations"""
    repo = DonationRepository(db)
    return repo.list_latest(skip=skip, limit=limit)


def get_total_donations(db: Session):
    """Calculer le total des donations"""
    repo = DonationRepository(db)
    return {"total_amount": repo.total_amount()}


def get_donation_stats(db: Session):
    """Statistiques des donations"""
    repo = DonationRepository(db)
    return repo.stats()
