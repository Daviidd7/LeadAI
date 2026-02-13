from __future__ import annotations

import json
import logging
from typing import Any, Dict

from openai import OpenAI, OpenAIError

from app.config import get_settings
from app.schemas import LeadCreate, LeadAIResult

logger = logging.getLogger(__name__)
settings = get_settings()

client = OpenAI(api_key=settings.openai_api_key)


def _build_prompt(lead: LeadCreate) -> str:
    return (
        "You are a senior B2B sales strategist. "
        "You receive inbound leads and must determine how qualified they are for a high-ticket B2B solution.\n\n"
        "Return a JSON object with these exact keys:\n"
        "- score: integer from 0 to 100 (higher is better fit)\n"
        "- priority: one of ['high', 'medium', 'low']\n"
        "- disqualified: boolean\n"
        "- summary: short summary (max 4 sentences) of why you rated the lead this way\n\n"
        "Consider:\n"
        "- Company size & type\n"
        "- Budget and timeline\n"
        "- Use case fit for an AI-powered automation/lead qualification solution\n"
        "- Buying intent and urgency\n\n"
        "Lead details:\n"
        f"Full name: {lead.full_name}\n"
        f"Email: {lead.email}\n"
        f"Company: {lead.company}\n"
        f"Website: {lead.website}\n"
        f"Phone: {lead.phone}\n"
        f"Budget: {lead.budget}\n"
        f"Timeline: {lead.timeline}\n"
        f"Use case: {lead.use_case}\n"
        f"Source: {lead.source}\n\n"
        "Respond with ONLY valid JSON, no additional text."
    )


def qualify_lead(lead: LeadCreate) -> LeadAIResult:
    prompt = _build_prompt(lead)
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are an expert B2B lead qualification assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )
    except OpenAIError as e:
        logger.error("OpenAI API error when qualifying lead: %s", e)
        raise

    try:
        content = response.choices[0].message.content or ""
        data: Dict[str, Any] = json.loads(content)
    except Exception as exc:
        logger.error("Failed to parse OpenAI response: %s", exc)
        logger.debug("Raw OpenAI response: %s", response)
        # Fallback conservative default
        data = {
            "score": 50,
            "priority": "medium",
            "disqualified": False,
            "summary": "Automatic fallback: could not parse AI output, please review manually.",
        }

    score = int(data.get("score", 50))
    score = max(0, min(100, score))
    priority = str(data.get("priority", "medium")).lower()
    if priority not in {"high", "medium", "low"}:
        priority = "medium"
    disqualified = bool(data.get("disqualified", False))
    summary = str(data.get("summary", ""))[:2000]

    ai_result = LeadAIResult(
        ai_score=score,
        ai_priority=priority,
        ai_summary=summary,
        ai_disqualified=disqualified,
        ai_raw_response=data,
    )
    return ai_result