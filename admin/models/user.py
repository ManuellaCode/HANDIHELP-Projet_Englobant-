from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..core.database import Base
from enum import Enum


class UserRole(str, Enum):
    DONOR = "donor"
    PARENT = "parent"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    role = Column(String, default=UserRole.DONOR)
    disability_type = Column(String, nullable=True)
    #created_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    donations = relationship("Donation", back_populates="user")
    assistance_requests = relationship("AssistanceRequest", back_populates="user")