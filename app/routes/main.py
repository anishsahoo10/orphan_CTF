from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import (
    ADMINISTRATOR,
    DOCUMENTATION_STATUS,
    LAST_MAINTENANCE,
    LAST_SYSTEM_UPDATE,
    NODE_ID,
    NODE_LOCATION,
    ORG_NAME,
    SYSTEM_STATUS,
    TEMPLATES_DIR,
)
from app.database import query_all, query_one
from app.routes.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_base_context(request: Request, page_title: str) -> dict:
    """Standard template context variables."""
    current_user = get_current_user(request)
    return {
        "page_title": page_title,
        "org_name": ORG_NAME,
        "node_id": NODE_ID,
        "node_location": NODE_LOCATION,
        "system_status": SYSTEM_STATUS,
        "administrator": ADMINISTRATOR,
        "doc_status": DOCUMENTATION_STATUS,
        "last_maintenance": LAST_MAINTENANCE,
        "last_system_update": LAST_SYSTEM_UPDATE,
        "current_user": current_user,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, q: Optional[str] = None):
    """Main Archive Search Page (Controlled SQL Injection point)."""
    context = get_base_context(request, "DECLASSIFIED ARCHIVES")
    
    sql_error = None
    if q is not None and q.strip() != "":
        # SQL Injection Point: Unsanitized concatenation
        try:
            raw_sql = (
                f"SELECT id, sender, recipient, timestamp, subject, classification, content "
                f"FROM messages "
                f"WHERE subject LIKE '%{q}%' OR content LIKE '%{q}%' "
                f"ORDER BY id ASC"
            )
            records = query_all(raw_sql)
        except Exception as e:
            records = []
            sql_error = str(e)
    else:
        # Default view: Standard public leaked records (hiding the confidential IT credentials)
        records = query_all(
            """
            SELECT id, sender, recipient, timestamp, subject, classification, content
            FROM messages
            WHERE classification != 'TOP SECRET // RESTRICTED ACCESS'
            ORDER BY id ASC
            """
        )
    
    context.update({
        "records": records,
        "search_query": q or "",
        "sql_error": sql_error,
    })
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@router.get("/mail", response_class=HTMLResponse)
async def mail_redirect(request: Request, q: Optional[str] = None):
    """Redirect /mail queries to root archive."""
    url = f"/?q={q}" if q else "/"
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/documents", response_class=HTMLResponse)
async def documents_redirect(request: Request):
    """Redirect legacy document path to root archive."""
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/flights", response_class=HTMLResponse)
async def flights_page(request: Request):
    """Private aviation registry & passenger flight manifests."""
    context = get_base_context(request, "FLIGHT MANIFESTS")
    flights = query_all("SELECT * FROM flights ORDER BY flight_date DESC")
    context.update({"flights": flights})
    return templates.TemplateResponse(
        request=request,
        name="flights.html",
        context=context,
    )


@router.get("/photos", response_class=HTMLResponse)
async def photos_page(request: Request):
    """Classified media vault (LOCKED - Requires Username & Password)."""
    user = get_current_user(request)
    
    # Check if user is authenticated
    if not user:
        context = get_base_context(request, "SURVEILLANCE VAULT (LOCKED)")
        return templates.TemplateResponse(
            request=request,
            name="photos_locked.html",
            context=context,
        )

    # If logged in, show unlocked photos & Flag 5
    context = get_base_context(request, "SURVEILLANCE EVIDENCE VAULT")
    photos = query_all("SELECT * FROM photos ORDER BY id ASC")
    context.update({"photos": photos})
    return templates.TemplateResponse(
        request=request,
        name="photos.html",
        context=context,
    )


@router.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    """Technical telemetry of node ATG-NODE-01."""
    context = get_base_context(request, "SYSTEM TELEMETRY")
    return templates.TemplateResponse(
        request=request,
        name="status.html",
        context=context,
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Authenticated executive console (requires session login)."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(
            url="/login?next=/dashboard",
            status_code=status.HTTP_302_FOUND,
        )

    context = get_base_context(request, "EXECUTIVE CONSOLE")
    users = query_all("SELECT id, username, role, created_at, last_login FROM users ORDER BY id ASC")
    flags = query_all("SELECT flag_name, flag_value, description FROM system_flags ORDER BY id ASC")
    
    context.update({
        "users": users,
        "flags": flags,
    })
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context,
    )
