from sqlalchemy.orm import Session

from ..models.child import Child
from .base import BaseRepository


class ChildRepository(BaseRepository[Child]):
    def __init__(self, db: Session):
        super().__init__(db, Child)

    def list_latest(self, skip: int = 0, limit: int = 100) -> list[Child]:
        return (
            self.db.query(Child)
            .order_by(Child.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_parent(self, parent_id: int, skip: int = 0, limit: int = 100) -> list[Child]:
        return (
            self.db.query(Child)
            .filter_by(parent_id=parent_id)
            .order_by(Child.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )