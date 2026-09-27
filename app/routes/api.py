from fastapi import APIRouter, HTTPException, status
from typing import List

from app.config import (
    ADMINISTRATOR,
    DOCUMENTATION_STATUS,
    LAST_MAINTENANCE,
    LAST_SYSTEM_UPDATE,
    NODE_ID,
    NODE_LOCATION,
    ORG_NAME,
    SYSTEM_STATUS,
)
from app.database import query_all, query_one

router = APIRouter(prefix="/api", tags=["internal-api"])


@router.get("/status")
async def get_system_status():
    """Retrieve operational telemetry for AXM-NODE-07."""
    services = query_all("SELECT name, status FROM system_services")
    active_count = sum(1 for s in services if s["status"] == "ACTIVE")
    
    return {
        "node_id": NODE_ID,
        "organization": ORG_NAME,
        "status": SYSTEM_STATUS,
        "location": NODE_LOCATION,
        "administrator": ADMINISTRATOR,
        "system_age": "UNKNOWN",
        "last_maintenance": LAST_MAINTENANCE,
        "last_system_update": LAST_SYSTEM_UPDATE,
        "documentation": DOCUMENTATION_STATUS,
        "services_online": active_count,
        "total_services": len(services),
    }


@router.get("/services")
async def get_system_services():
    """Retrieve active system service status and daemon bindings."""
    services = query_all("SELECT id, name, status, version, last_check, owner FROM system_services ORDER BY id ASC")
    return {"services": services}


@router.get("/documents")
async def get_documents_metadata():
    """Retrieve indexed document metadata."""
    docs = query_all(
        """
        SELECT id, slug, title, classification, category, created_date, author
        FROM documents
        ORDER BY id ASC
        """
    )
    return {"documents": docs}


@router.get("/documents/{slug}")
async def get_document_by_slug(slug: str):
    """Retrieve specific archival document by slug."""
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
            detail=f"Document slug '{slug}' not found in archive registry.",
        )
    return {"document": doc}
