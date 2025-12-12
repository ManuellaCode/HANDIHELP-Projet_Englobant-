from datetime import datetime,UTC
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AssistanceRequest(Base):
    __tablename__ = "assistance_requests"  # Pluriel

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ForeignKey
    category = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")  # pending | approved | rejected
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relation
    user = relationship("User", back_populates="assistance_requests")