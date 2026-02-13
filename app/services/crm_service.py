from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.config import get_settings
from app.schemas import LeadOut

logger = logging.getLogger(__name__)
settings = get_settings()


async def push_lead_to_crm(lead: LeadOut) -> Optional[str]:
    if not (settings.crm_base_url and settings.crm_api_key):
        logger.info("CRM not configured; skipping CRM sync")
        return None

    payload = {
        "properties": {
            "email": lead.email,
            "firstname": lead.full_name,
            "company": lead.company or "",
            "phone": lead.phone or "",
            "website": lead.website or "",
            "lifecyclestage": "lead",
            "lead_source": lead.source or "website",
            "ai_score": lead.ai_score,
            "ai_priority": lead.ai_priority,
            "ai_disqualified": lead.ai_disqualified,
            "use_case": lead.use_case,
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.crm_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(3):
            try:
                resp = await client.post(settings.crm_base_url, json=payload, headers=headers)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    external_id = str(data.get("id") or data.get("objectId") or "")
                    logger.info("Pushed lead %s to CRM with id %s", lead.id, external_id)
                    return external_id
                elif resp.status_code in (429, 500, 502, 503, 504):
                    logger.warning(
                        "Transient CRM error (status %s), attempt %s: %s",
                        resp.status_code,
                        attempt + 1,
                        resp.text,
                    )
                else:
                    logger.error(
                        "Permanent CRM error (status %s): %s", resp.status_code, resp.text
                    )
                    return None
            except httpx.RequestError as exc:
                logger.error("CRM request error on attempt %s: %s", attempt + 1, exc)
        logger.error("Failed to push lead %s to CRM after retries", lead.id)
        return None