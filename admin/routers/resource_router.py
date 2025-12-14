from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.resource_schema import ResourceCreate, ResourceOut
from ..services.resource_service import create_resource, search_resources

router = APIRouter(prefix="/admin/resources", tags=["Resource Management"])


@router.post("/", response_model=ResourceOut, status_code=status.HTTP_201_CREATED)
def create(payload: ResourceCreate, db: Session = Depends(get_db)):
    return create_resource(db, payload)


@router.get("/", response_model=list[ResourceOut])
def search(
    handicap_type: str | None = None,
    resource_type: str | None = None,
    region: str | None = None,
    db: Session = Depends(get_db),
):
    return search_resources(db, handicap_type, resource_type, region)
