from __future__ import annotations

from typing import Optional, Any, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LeadBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    company: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    use_case: str = Field(..., min_length=10)
    source: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadAIResult(BaseModel):
    ai_score: int
    ai_priority: str
    ai_summary: str
    ai_disqualified: bool
    ai_raw_response: Any


class LeadOut(LeadBase):
    id: UUID
    ai_score: Optional[int] = None
    ai_priority: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_disqualified: bool
    status: str

    class Config:
        from_attributes = True


class LeadList(BaseModel):
    leads: List[LeadOut]


class AdminLoginForm(BaseModel):
    username: str
    password: str