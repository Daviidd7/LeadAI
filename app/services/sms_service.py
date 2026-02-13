from __future__ import annotations

import logging
from typing import Optional

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

from app.config import get_settings
from app.schemas import LeadOut

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_client() -> Optional[Client]:
    if not (settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_from_number and settings.twilio_sales_number):
        return None
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_lead_notification_sms(lead: LeadOut) -> None:
    client = _get_client()
    if client is None:
        logger.info("Twilio not configured; skipping SMS notification")
        return

    body = (
        f"New lead: {lead.full_name} ({lead.company or 'N/A'})\n"
        f"Score: {lead.ai_score} ({lead.ai_priority})\n"
        f"Email: {lead.email}\n"
        f"Use case: {lead.use_case[:120]}..."
    )

    try:
        client.messages.create(
            body=body,
            from_=settings.twilio_from_number,
            to=settings.twilio_sales_number,
        )
        logger.info("Lead notification SMS sent for lead %s", lead.id)
    except TwilioException as exc:
        logger.error("Failed to send SMS notification: %s", exc)