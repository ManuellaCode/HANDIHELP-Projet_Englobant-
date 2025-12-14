from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False, index=True)
    # ex: association, professionnel, centre, service

    description = Column(String, nullable=True)

    handicap_id = Column(Integer, ForeignKey("handicap.id"), nullable=True, index=True)

    region = Column(String, nullable=True, index=True)
    city = Column(String, nullable=True)

    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)

    validated = Column(Boolean, default=True)  # admin only for now

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    handicap = relationship("Handicap")
