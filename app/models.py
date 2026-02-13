from __future__ import annotations

import datetime as dt
import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=dt.datetime.utcnow)

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    budget = Column(String(255), nullable=True)
    timeline = Column(String(255), nullable=True)
    use_case = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)

    ai_score = Column(Integer, nullable=True)
    ai_priority = Column(String(20), nullable=True)
    ai_summary = Column(Text, nullable=True)
    ai_disqualified = Column(Boolean, nullable=False, default=False)
    ai_raw_response = Column(JSONB, nullable=True)

    crm_external_id = Column(String(255), nullable=True)
    crm_status = Column(String(50), nullable=True)

    status = Column(String(50), nullable=False, default="new")