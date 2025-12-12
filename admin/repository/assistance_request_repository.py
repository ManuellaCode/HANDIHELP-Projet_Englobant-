from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.AssistanceRequest import AssistanceRequest
from .base import BaseRepository


class AssistanceRequestRepository(BaseRepository[AssistanceRequest]):
    def __init__(self, db: Session):
        super().__init__(db, AssistanceRequest)

    def list_latest(self, skip: int = 0, limit: int = 100) -> List[AssistanceRequest]:
        return (
            self.db.query(AssistanceRequest)
            .order_by(AssistanceRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_status(
        self, status_value: str, skip: int = 0, limit: int = 100
    ) -> List[AssistanceRequest]:
        return (
            self.db.query(AssistanceRequest)
            .filter_by(status=status_value)
            .order_by(AssistanceRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, request_id: int) -> Optional[AssistanceRequest]:
        return self.get(request_id)