from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.AssistanceRequest import RequestStatus
from ..repository.assistance_request_repository import AssistanceRequestRepository


def list_requests(
    db: Session,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """Lister les demandes d'assistance"""
    repo = AssistanceRequestRepository(db)

    if status_filter:
        try:
            status_enum = RequestStatus(status_filter)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}",
            )
        return repo.list_by_status(status_enum.value, skip=skip, limit=limit)

    return repo.list_latest(skip=skip, limit=limit)


def update_request_status(db: Session, request_id: int, new_status: str):
    """Mettre à jour le statut d'une demande"""
    repo = AssistanceRequestRepository(db)

    try:
        status_enum = RequestStatus(new_status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status: {new_status}",
        )

    assistance_request = repo.get_by_id(request_id)
    if not assistance_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    assistance_request.status = status_enum.value
    db.commit()
    db.refresh(assistance_request)
    return assistance_request