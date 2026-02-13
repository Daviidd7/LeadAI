from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz() -> None:
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_lead_validation() -> None:
    payload = {
        "full_name": "T",
        "email": "invalid",
        "use_case": "short",
    }
    resp = client.post("/api/leads", json=payload)
    assert resp.status_code == 422