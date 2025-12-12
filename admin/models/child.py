from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..core.database import Base

class Child(Base):
    __tablename__ = "child"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    age = Column(Integer)
    handicap_id = Column(Integer, ForeignKey("handicap.id"))
    parent_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))