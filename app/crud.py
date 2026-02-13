from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


def create_lead(db: Session, lead_in: schemas.LeadCreate) -> models.Lead:
    lead = models.Lead(
        full_name=lead_in.full_name.strip(),
        email=lead_in.email.strip().lower(),
        company=(lead_in.company or "").strip() or None,
        website=(lead_in.website or "").strip() or None,
        phone=(lead_in.phone or "").strip() or None,
        budget=(lead_in.budget or "").strip() or None,
        timeline=(lead_in.timeline or "").strip() or None,
        use_case=lead_in.use_case.strip(),
        source=(lead_in.source or "").strip() or None,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def update_lead_ai_result(
    db: Session, lead: models.Lead, ai_result: schemas.LeadAIResult
) -> models.Lead:
    lead.ai_score = ai_result.ai_score
    lead.ai_priority = ai_result.ai_priority
    lead.ai_summary = ai_result.ai_summary
    lead.ai_disqualified = ai_result.ai_disqualified
    lead.ai_raw_response = ai_result.ai_raw_response
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def set_lead_crm_info(
    db: Session, lead: models.Lead, external_id: str, status: str
) -> models.Lead:
    lead.crm_external_id = external_id
    lead.crm_status = status
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def list_leads(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    min_score: Optional[int] = None,
    priority: Optional[str] = None,
) -> List[models.Lead]:
    query = db.query(models.Lead).order_by(models.Lead.created_at.desc())
    if min_score is not None:
        query = query.filter(models.Lead.ai_score >= min_score)
    if priority:
        query = query.filter(models.Lead.ai_priority == priority)
    return query.offset(offset).limit(limit).all()