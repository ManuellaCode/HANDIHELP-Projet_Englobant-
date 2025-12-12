from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime
from ..core.database import Base


class Handicap(Base):
    __tablename__ = "handicap"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))