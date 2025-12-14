from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.resource_service import get_total_resources
from ..core.security import require_admin  # ou équivalent

router = APIRouter(
    prefix="/admin/stats/resources",
    tags=["Admin - Resource Stats"]
)


@router.get("/total")
def total_resources(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    return get_total_resources(db)
