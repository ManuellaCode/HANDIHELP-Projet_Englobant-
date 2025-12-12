from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base


class Donation(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    donor_name = Column(String, nullable=True, index=True)
    donor_email = Column(String, nullable=True, index=True)

    amount = Column(Float, nullable=False)
    message = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="donations")