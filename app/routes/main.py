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
async def home_page(request: Request):
    """Public-facing entry point to the legacy internal resource node."""
    context = get_base_context(request, "INTERNAL RESOURCE NODE")
    
    services = query_all("SELECT name, status, version FROM system_services ORDER BY id ASC")
    doc_count = query_one("SELECT COUNT(*) as count FROM documents")
    
    context.update({
        "services": services,
        "doc_count": doc_count["count"] if doc_count else 0,
    })
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@router.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    """Detailed technical status of internal subsystems and daemons."""
    context = get_base_context(request, "SYSTEM STATUS")
    
    services = query_all("SELECT * FROM system_services ORDER BY id ASC")
    audit_count = query_one("SELECT COUNT(*) as count FROM audit_logs")
    
    context.update({
        "services": services,
        "audit_count": audit_count["count"] if audit_count else 0,
    })
    return templates.TemplateResponse(
        request=request,
        name="status.html",
        context=context,
    )


@router.get("/documents", response_class=HTMLResponse)
async def documents_page(request: Request, q: Optional[str] = None):
    """Internal archival document repository with search capability (Controlled SQL Injection point)."""
    context = get_base_context(request, "DOCUMENTATION ARCHIVE")
    
    sql_error = None
    if q is not None and q.strip() != "":
        # Controlled SQL Injection point: unescaped legacy query concatenation
        try:
            raw_sql = f"SELECT id, slug, title, classification, category, created_date, author FROM documents WHERE title LIKE '%{q}%' OR content LIKE '%{q}%' ORDER BY id ASC"
            docs = query_all(raw_sql)
        except Exception as e:
            docs = []
            sql_error = str(e)
    else:
        docs = query_all(
            """
            SELECT id, slug, title, classification, category, created_date, author
            FROM documents
            ORDER BY id ASC
            """
        )
    
    context.update({
        "documents": docs,
        "search_query": q or "",
        "sql_error": sql_error,
    })
    return templates.TemplateResponse(
        request=request,
        name="documents.html",
        context=context,
    )


@router.get("/documents/{slug}", response_class=HTMLResponse)
async def document_detail_page(request: Request, slug: str):
    """Individual archival document reader."""
    doc = query_one(
        """
        SELECT id, slug, title, classification, category, content, created_date, author
        FROM documents
        WHERE slug = ?
        """,
        (slug,),
    )
    
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DOCUMENT '{slug}' NOT FOUND IN ARCHIVAL STORE",
        )
    
    context = get_base_context(request, f"DOC // {doc['slug'].upper()}")
    context.update({"document": doc})
    return templates.TemplateResponse(
        request=request,
        name="document_detail.html",
        context=context,
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Internal employee dashboard with dense tabular data (authentication required)."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(
            url="/login?next=/dashboard",
            status_code=status.HTTP_302_FOUND,
        )

    context = get_base_context(request, "EMPLOYEE DASHBOARD")
    
    employees = query_all("SELECT * FROM employees ORDER BY employee_id ASC")
    services = query_all("SELECT * FROM system_services ORDER BY id ASC")
    documents = query_all("SELECT id, slug, title, classification, category, created_date FROM documents ORDER BY id ASC")
    recent_logs = query_all("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 10")
    
    context.update({
        "employees": employees,
        "services": services,
        "documents": documents,
        "recent_logs": recent_logs,
    })
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context,
    )
