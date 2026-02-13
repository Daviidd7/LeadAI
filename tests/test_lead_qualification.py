from __future__ import annotations

from app.schemas import LeadCreate
from app.services.ai_qualification import _build_prompt


def test_prompt_contains_required_fields() -> None:
  lead = LeadCreate(
      full_name="Test User",
      email="test@example.com",
      company="TestCo",
      website="https://test.com",
      phone="+10000000000",
      budget="5-15k",
      timeline="1-3months",
      use_case="We want to qualify leads using AI.",
      source="test",
  )
  prompt = _build_prompt(lead)
  assert "Test User" in prompt
  assert "test@example.com" in prompt
  assert "We want to qualify leads using AI." in prompt