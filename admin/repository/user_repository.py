from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.user import User, UserRole
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def list_non_admins(self, skip: int = 0, limit: int = 100) -> List[User]:
        return (
            self.db.query(User)
            .filter(User.role.in_([UserRole.DONOR, UserRole.PARENT]))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_admins(self, skip: int = 0, limit: int = 100) -> List[User]:
        return (
            self.db.query(User)
            .filter_by(role=UserRole.ADMIN)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter_by(email=email).first()