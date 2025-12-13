from datetime import datetime, UTC

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)

    handicap_id = Column(Integer, ForeignKey("handicap.id"), nullable=True, index=True)

    age_min = Column(Integer, nullable=True)
    age_max = Column(Integer, nullable=True)

    content = Column(Text, nullable=False)

    source_url = Column(String, nullable=True)
    tags = Column(String, nullable=True)

    published = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    handicap = relationship("Handicap")