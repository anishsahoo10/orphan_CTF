from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.config import (
    ADMINISTRATOR,
    DOCUMENTATION_STATUS,
    HOST,
    LAST_MAINTENANCE,
    LAST_SYSTEM_UPDATE,
    NODE_ID,
    NODE_LOCATION,
    ORG_NAME,
    PORT,
    SECRET_KEY,
    SESSION_COOKIE_NAME,
    STATIC_DIR,
    SYSTEM_STATUS,
    TEMPLATES_DIR,
)
from app.database import ensure_database_exists
from app.routes.api import router as api_router
from app.routes.auth import router as auth_router
from app.routes.main import router as main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database is present on startup
    ensure_database_exists()
    yield


app = FastAPI(
    title="AETHELGARD ARCHIVES",
    description="The Archipelago Network // Investigative Leak Portal",
    version="2.1.0-leak",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# Custom Middleware to inject Flag 1 header into all HTTP responses and handle HEAD
@app.middleware("http")
async def add_ctf_recon_header(request: Request, call_next):
    is_head = request.method == "HEAD"
    if is_head:
        request.scope["method"] = "GET"
    response = await call_next(request)
    if is_head:
        response.body = b""
        response.headers["content-length"] = "0"
    response.headers["X-Apex-Telemetry"] = "flag{4rch1p3l4g0_r3c0n_f1ng3rpr1nt_88a1}"
    response.headers["X-Archipelago-Node"] = "flag{4rch1p3l4g0_r3c0n_f1ng3rpr1nt_88a1}"
    response.headers["X-Node-Origin"] = "APEX-SITE-BRAVO-TEST-RANGE"
    return response

# Mount Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie=SESSION_COOKIE_NAME,
    max_age=86400,
    same_site="lax",
    https_only=False,
)

# Mount Static Files
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Mount Routers
app.include_router(main_router)
app.include_router(auth_router)
app.include_router(api_router)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """Robots.txt directing recon scanners to leaked compartments."""
    return (
        "User-agent: *\n"
        "Disallow: /api/\n"
        "Disallow: /mail/\n"
        "Disallow: /flights/\n"
        "Disallow: /photos/\n"
        "Disallow: /dashboard/\n"
    )


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    """Custom 404 handler tailored for the clean investigative archive look."""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "RESOURCE_UNINDEXED",
                "reference": "ATG-01",
                "detail": str(exc.detail) if hasattr(exc, "detail") else "Not Found",
            },
        )
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "page_title": "ARCHIVE ENTRY NOT FOUND",
            "org_name": ORG_NAME,
            "node_id": NODE_ID,
            "error_code": "ENTRY_UNINDEXED",
            "error_detail": getattr(exc, "detail", "The requested leaked dossier or manifest could not be retrieved."),
            "reference": "ATG-01",
            "system_status": SYSTEM_STATUS,
            "current_user": None,
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(500)
async def custom_500_handler(request: Request, exc: Exception):
    """Custom 500 handler."""
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "page_title": "ARCHIVE PROCESSING FAULT",
            "org_name": ORG_NAME,
            "node_id": NODE_ID,
            "error_code": "DISPATCH_FAULT",
            "error_detail": "Internal database or parser processing exception.",
            "reference": "ATG-01",
            "system_status": SYSTEM_STATUS,
            "current_user": None,
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
