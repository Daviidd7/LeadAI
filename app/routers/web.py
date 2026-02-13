from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_admin_user, get_db
from app.rate_limiter import limit_requests
from app.services.ai_qualification import qualify_lead

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def lead_form(request: Request) -> Any:
    return templates.TemplateResponse("lead_form.html", {"request": request})


@router.post("/submit", response_class=HTMLResponse, dependencies=[Depends(limit_requests)])
async def submit_lead_form(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    website: str = Form(""),
    phone: str = Form(""),
    budget: str = Form(""),
    timeline: str = Form(""),
    use_case: str = Form(...),
    source: str = Form("website"),
    db: Session = Depends(get_db),
) -> Any:
    lead_in = schemas.LeadCreate(
        full_name=full_name,
        email=email,
        company=company or None,
        website=website or None,
        phone=phone or None,
        budget=budget or None,
        timeline=timeline or None,
        use_case=use_case,
        source=source,
    )
    lead = crud.create_lead(db, lead_in)
    try:
        ai_result = qualify_lead(lead_in)
        crud.update_lead_ai_result(db, lead, ai_result)
    except Exception:
        pass
    return templates.TemplateResponse("thank_you.html", {"request": request})


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request) -> Any:
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
) -> Any:
    from app.config import get_settings

    settings = get_settings()
    if username == settings.admin_username and password == settings.admin_password:
        response = RedirectResponse(url="/admin/leads", status_code=302)
        # Simple cookie-based flag; for production, use signed sessions.
        response.set_cookie("admin_auth", "1", httponly=True, max_age=3600)
        return response
    return templates.TemplateResponse(
        "admin_login.html",
        {"request": request, "error": "Invalid username or password"},
        status_code=401,
    )


def _require_admin(request: Request) -> None:
    if request.cookies.get("admin_auth") != "1":
        raise RedirectResponse(url="/admin/login", status_code=302)


@router.get("/admin/leads", response_class=HTMLResponse)
async def admin_leads_page(
    request: Request,
    min_score: Optional[int] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
) -> Any:
    _require_admin(request)
    leads = crud.list_leads(db, limit=200, offset=0, min_score=min_score, priority=priority)
    leads_out = [schemas.LeadOut.model_validate(l) for l in leads]
    context: Dict[str, Any] = {
        "request": request,
        "leads": leads_out,
        "min_score": min_score or "",
        "priority": priority or "",
    }
    return templates.TemplateResponse("admin_dashboard.html", context)