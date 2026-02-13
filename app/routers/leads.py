from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, BackgroundTasks, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_db
from app.rate_limiter import limit_requests
from app.services.ai_qualification import qualify_lead
from app.services.email_service import send_lead_notification_email
from app.services.sms_service import send_lead_notification_sms
from app.services.crm_service import push_lead_to_crm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("", response_model=schemas.LeadOut, dependencies=[Depends(limit_requests)])
async def create_lead_endpoint(
    lead_in: schemas.LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> schemas.LeadOut:
    lead = crud.create_lead(db, lead_in)
    logger.info("Created new lead %s", lead.id)

    try:
        ai_result = qualify_lead(lead_in)
        lead = crud.update_lead_ai_result(db, lead, ai_result)
    except Exception as exc:
        logger.error("Error during AI qualification: %s", exc)

    lead_out = schemas.LeadOut.model_validate(lead)

    background_tasks.add_task(send_lead_notification_email, lead_out)
    background_tasks.add_task(send_lead_notification_sms, lead_out)
    background_tasks.add_task(_push_to_crm_background, lead_out, lead.id, db)

    return lead_out


def _push_to_crm_background(lead_out: schemas.LeadOut, lead_id: Any, db: Session) -> None:
    import asyncio

    async def _run() -> None:
        external_id = await push_lead_to_crm(lead_out)
        if external_id:
            from app import models  # local import to avoid cycles

            lead_db = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
            if lead_db:
                from app.crud import set_lead_crm_info

                set_lead_crm_info(db, lead_db, external_id, status="synced")

    try:
        asyncio.run(_run())
    except RuntimeError:
        # Already in an event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_run())


@router.get("", response_model=schemas.LeadList, dependencies=[Depends(limit_requests)])
def list_leads_endpoint(
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0,
    min_score: int | None = None,
    priority: str | None = None,
) -> schemas.LeadList:
    leads = crud.list_leads(db, limit=limit, offset=offset, min_score=min_score, priority=priority)
    return schemas.LeadList(leads=[schemas.LeadOut.model_validate(l) for l in leads])


@router.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}