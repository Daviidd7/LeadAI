from __future__ import annotations

from app.config import get_settings
from app.database import get_db
from app.schemas import LeadCreate
from app import crud

settings = get_settings()


def run() -> None:
    sample_leads = [
        LeadCreate(
            full_name="Alice Johnson",
            email="alice@examplecorp.com",
            company="ExampleCorp",
            website="https://examplecorp.com",
            phone="+12025550123",
            budget="15-50k",
            timeline="1-3months",
            use_case="We want to qualify leads from our website and prioritize prospects with >50 employees.",
            source="seed",
        ),
        LeadCreate(
            full_name="Bob Smith",
            email="bob@smallagency.io",
            company="SmallAgency",
            website="https://smallagency.io",
            phone="+12025550124",
            budget="<5k",
            timeline=">6months",
            use_case="Curious about AI but we don't have budget yet. Maybe a small proof-of-concept.",
            source="seed",
        ),
    ]
    with get_db() as db:
        for lead in sample_leads:
            crud.create_lead(db, lead)
    print("Seed data inserted.")


if __name__ == "__main__":
    run()