from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.assistance_schema import AssistanceRequestOut, StatusUpdate
from ..services.assistance_service import list_requests, update_request_status

router = APIRouter(prefix="/admin/requests", tags=["Assistance Requests"])


@router.get("/", response_model=list[AssistanceRequestOut])
def get_requests(
    status_filter: str = Query(None, description="pending | approved | rejected"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lister les demandes d'assistance"""
    return list_requests(db, status_filter, skip, limit)


@router.put("/{request_id}/status", response_model=AssistanceRequestOut)
def change_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour le statut d'une demande"""
    return update_request_status(db, request_id, status_update.status)
