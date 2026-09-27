from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.database import execute, query_one
from app.utils.auth import verify_password

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_current_user(request: Request) -> Optional[dict]:
    """Retrieve current authenticated user from session, if valid."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = query_one(
        "SELECT id, username, role, created_at, last_login FROM users WHERE id = ?",
        (user_id,),
    )
    return user


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: Optional[str] = None):
    """Render the employee authentication interface."""
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "page_title": "EMPLOYEE AUTHENTICATION",
            "next_url": next or "/dashboard",
            "error": None,
            "current_user": None,
        },
    )


@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: Optional[str] = Form(None),
):
    """Process employee credentials securely."""
    # Look up user securely by username
    user = query_one(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username.strip(),),
    )

    client_ip = request.client.host if request.client else "127.0.0.1"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not user or not verify_password(password, user["password_hash"]):
        # Log failed attempt in audit log
        execute(
            """
            INSERT INTO audit_logs (timestamp, event_type, source_ip, details)
            VALUES (?, 'AUTH_FAILED', ?, ?)
            """,
            (now_str, client_ip, f"Authentication failed for user identifier: '{username.strip()}'"),
        )
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "page_title": "EMPLOYEE AUTHENTICATION",
                "next_url": next or "/dashboard",
                "error": "AUTHENTICATION REJECTED: Invalid credentials or account locked.",
                "username": username,
                "current_user": None,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Establish session
    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]

    # Update last login timestamp
    execute("UPDATE users SET last_login = ? WHERE id = ?", (now_str, user["id"]))

    # Record successful login
    execute(
        """
        INSERT INTO audit_logs (timestamp, event_type, source_ip, details)
        VALUES (?, 'AUTH_SUCCESS', ?, ?)
        """,
        (now_str, client_ip, f"User '{user['username']}' established authenticated session"),
    )

    target_url = next if (next and next.startswith("/")) else "/dashboard"
    return RedirectResponse(url=target_url, status_code=status.HTTP_302_FOUND)


@router.get("/logout")
async def logout(request: Request):
    """Terminate the authenticated session."""
    user = get_current_user(request)
    if user:
        client_ip = request.client.host if request.client else "127.0.0.1"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execute(
            """
            INSERT INTO audit_logs (timestamp, event_type, source_ip, details)
            VALUES (?, 'AUTH_LOGOUT', ?, ?)
            """,
            (now_str, client_ip, f"User '{user['username']}' closed session"),
        )

    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
