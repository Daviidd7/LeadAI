from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from app.config import get_settings
from app.schemas import LeadOut

logger = logging.getLogger(__name__)
settings = get_settings()


def send_lead_notification_email(lead: LeadOut) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"[New Lead] {lead.full_name} ({lead.company or 'No company'})"
    msg["From"] = settings.smtp_from_email
    msg["To"] = settings.lead_notification_email

    body_lines = [
        f"New lead submitted:",
        "",
        f"Name: {lead.full_name}",
        f"Email: {lead.email}",
        f"Company: {lead.company}",
        f"Website: {lead.website}",
        f"Phone: {lead.phone}",
        f"Budget: {lead.budget}",
        f"Timeline: {lead.timeline}",
        f"Use case: {lead.use_case}",
        "",
        f"AI score: {lead.ai_score}",
        f"AI priority: {lead.ai_priority}",
        f"AI disqualified: {lead.ai_disqualified}",
        f"Status: {lead.status}",
    ]
    msg.set_content("\n".join(body_lines))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        logger.info("Lead notification email sent for lead %s", lead.id)
    except Exception as exc:
        logger.error("Failed to send lead notification email: %s", exc)