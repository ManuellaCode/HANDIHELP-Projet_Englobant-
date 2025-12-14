from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.handicap import Handicap
from ..models.resource import Resource
from ..repository.resource_repository import ResourceRepository
from ..schemas.resource_schema import ResourceCreate, ResourceUpdate


def _handicap_id_from_type(db: Session, handicap_type: str | None) -> int | None:
    if handicap_type is None:
        return None
    handicap = db.query(Handicap).filter_by(name=handicap_type).first()
    if not handicap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown handicap_type: {handicap_type}",
        )
    return handicap.id


def _fill_handicap_type(resource: Resource):
    if resource.handicap:
        resource.handicap_type = resource.handicap.name
    else:
        resource.handicap_type = None


def create_resource(db: Session, payload: ResourceCreate) -> Resource:
    repo = ResourceRepository(db)

    handicap_id = _handicap_id_from_type(
        db, payload.handicap_type.value if payload.handicap_type else None
    )

    resource = Resource(
        name=payload.name,
        resource_type=payload.resource_type,
        description=payload.description,
        handicap_id=handicap_id,
        region=payload.region,
        city=payload.city,
        phone=payload.phone,
        email=str(payload.email) if payload.email else None,
        website=str(payload.website) if payload.website else None,
        validated=payload.validated,
    )

    created = repo.create(resource)
    _fill_handicap_type(created)
    return created


def search_resources(
    db: Session,
    handicap_type: str | None = None,
    resource_type: str | None = None,
    region: str | None = None,
):
    handicap_id = _handicap_id_from_type(db, handicap_type) if handicap_type else None
    repo = ResourceRepository(db)
    items = repo.search(handicap_id, resource_type, region)
    for r in items:
        _fill_handicap_type(r)
    return items

def get_total_resources(db: Session) -> dict:
    repo = ResourceRepository(db)
    total = repo.count_all()

    return {
        "total_resources": total
    }