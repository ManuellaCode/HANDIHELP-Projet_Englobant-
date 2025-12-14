from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from ..models.resource import Resource
from .base import BaseRepository


class ResourceRepository(BaseRepository[Resource]):
    def __init__(self, db: Session):
        super().__init__(db, Resource)

    def search(
        self,
        handicap_id: int | None = None,
        resource_type: str | None = None,
        region: str | None = None,
    ) -> list[Resource]:
        query = self.db.query(Resource)

        if handicap_id:
            query = query.filter(Resource.handicap_id == handicap_id)
        if resource_type:
            query = query.filter(Resource.resource_type == resource_type)
        if region:
            query = query.filter(Resource.region.ilike(f"%{region}%"))

        return query.order_by(Resource.created_at.desc()).all()

    def count_all(self) -> int:
        return self.db.query(func.count(Resource.id)).scalar()
