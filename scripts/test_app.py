"""Comprehensive route and functional test suite for ORPHAN - Strong Coffee (LEGACY TELECOM)."""
import sys
from pathlib import Path
from starlette.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app

def run_tests():
    print("=" * 60)
    print("STARTING TEST SUITE: ORPHAN - Strong Coffee (LEGACY TELECOM)")
    print("=" * 60)

    client = TestClient(app, follow_redirects=False)

    passed = 0
    total = 0

    def assert_check(name: str, condition: bool, details: str = ""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}: {details}")

    # 1. Gateway Page (/)
    res = client.get("/")
    assert_check("GET / returns 200", res.status_code == 200)
    assert_check("GET / contains STRONG COFFEE", "STRONG COFFEE" in res.text)
    assert_check("GET / contains SCF-NODE-07", "SCF-NODE-07" in res.text)
    assert_check("GET / contains INTERNAL RESOURCE NODE", "INTERNAL RESOURCE NODE" in res.text)

    # 2. Robots.txt (Reconnaissance)
    res = client.get("/robots.txt")
    assert_check("GET /robots.txt returns 200", res.status_code == 200)
    assert_check("GET /robots.txt disallows /documents/", "Disallow: /documents/" in res.text)
    assert_check("GET /robots.txt disallows /api/", "Disallow: /api/" in res.text)

    # 3. System Status Page (/status)
    res = client.get("/status")
    assert_check("GET /status returns 200", res.status_code == 200)
    assert_check("GET /status lists WEB-NODE", "WEB-NODE" in res.text)
    assert_check("GET /status lists DATABASE", "DATABASE" in res.text)
    assert_check("GET /status lists AUTHENTICATION", "AUTHENTICATION" in res.text)

    # 4. Documents Archive (/documents)
    res = client.get("/documents")
    assert_check("GET /documents returns 200", res.status_code == 200)
    assert_check("GET /documents lists system-overview", "system-overview" in res.text)
    assert_check("GET /documents lists maintenance-log", "maintenance-log" in res.text)

    # 5. Documents Search (Legitimate keyword filter)
    res = client.get("/documents?q=system")
    assert_check("GET /documents?q=system returns 200", res.status_code == 200)
    assert_check("Filtered results contain system-overview", "system-overview" in res.text)

    # 6. SQL Injection - Syntax Error triggering
    res = client.get("/documents?q='")
    assert_check("GET /documents?q=' returns 200 with error block", res.status_code == 200)
    assert_check("SQL syntax error displayed in page", "unrecognized token" in res.text or "syntax error" in res.text.lower())

    # 7. SQL Injection - Boolean Bypass (' OR '1'='1)
    res = client.get("/documents?q=' OR '1'='1")
    assert_check("GET /documents?q=' OR '1'='1 returns 200", res.status_code == 200)
    assert_check("SQLi boolean bypass returns documents", "system-overview" in res.text and "maintenance-log" in res.text)

    # 8. SQL Injection - UNION extraction of system_flags
    payload = "' UNION SELECT 999, 'flag-doc', flag_name, flag_value, 'FLAG', '2026-01-01', 'root' FROM system_flags--"
    res = client.get(f"/documents?q={payload}")
    assert_check("GET /documents with UNION injection returns 200", res.status_code == 200)
    assert_check("UNION injection extracts USER_FLAG", "USER_FLAG" in res.text)
    assert_check("UNION injection extracts user flag value", "flag{str0ng_c0ff33_sql1_untr4ck3d_n0d3_994c}" in res.text)

    # 9. Individual Document Detail (/documents/system-overview)
    res = client.get("/documents/system-overview")
    assert_check("GET /documents/system-overview returns 200", res.status_code == 200)
    assert_check("GET /documents/system-overview contains Daniel Mercer", "Daniel Mercer" in res.text)
    assert_check("GET /documents/system-overview contains MO-2018-99", "MO-2018-99" in res.text)

    # 10. Non-existent Document -> 404 with custom error page
    res = client.get("/documents/non-existent-secret-doc")
    assert_check("GET /documents/non-existent-doc returns 404", res.status_code == 404)
    assert_check("404 page contains NODE_UNAVAILABLE", "NODE_UNAVAILABLE" in res.text)

    # 11. Unauthenticated Dashboard Access (/dashboard)
    res = client.get("/dashboard")
    assert_check("GET /dashboard redirects when unauthenticated", res.status_code == 302)
    assert_check("GET /dashboard redirects to /login", "/login" in res.headers.get("location", ""))

    # 12. Login Page (/login)
    res = client.get("/login")
    assert_check("GET /login returns 200", res.status_code == 200)
    assert_check("GET /login contains EMPLOYEE AUTHENTICATION", "EMPLOYEE AUTHENTICATION" in res.text)

    # 13. Failed Login Attempt
    res = client.post("/login", data={"username": "operator", "password": "wrong_password"})
    assert_check("POST /login with bad credentials returns 401", res.status_code == 401)
    assert_check("POST /login error message rendered", "AUTHENTICATION REJECTED" in res.text)

    # 14. Successful Login as d.mercer using cracked password (telecom2019)
    res = client.post("/login", data={"username": "d.mercer", "password": "telecom2019"})
    assert_check("POST /login as d.mercer redirects (302)", res.status_code == 302)
    assert_check("POST /login redirects to dashboard", res.headers.get("location") == "/dashboard")
    assert_check("POST /login sets session cookie", "scf_session" in client.cookies)

    # 15. Authenticated Dashboard Access
    res = client.get("/dashboard")
    assert_check("GET /dashboard with d.mercer session returns 200", res.status_code == 200)
    assert_check("GET /dashboard contains d.mercer session info", "d.mercer" in res.text)
    assert_check("GET /dashboard lists Daniel Mercer", "Daniel Mercer" in res.text)
    assert_check("GET /dashboard contains SYSTEM AUDIT JOURNAL", "SYSTEM AUDIT JOURNAL" in res.text)

    # 16. API Endpoints
    res = client.get("/api/status")
    assert_check("GET /api/status returns 200", res.status_code == 200)
    assert_check("GET /api/status has correct node_id", res.json().get("node_id") == "SCF-NODE-07")

    res = client.get("/api/services")
    assert_check("GET /api/services returns 200", res.status_code == 200)
    assert_check("GET /api/services returns 5 services", len(res.json().get("services", [])) == 5)

    res = client.get("/api/documents")
    assert_check("GET /api/documents returns 200", res.status_code == 200)
    assert_check("GET /api/documents returns 5 documents", len(res.json().get("documents", [])) == 5)

    # 17. Logout (/logout)
    res = client.get("/logout")
    assert_check("GET /logout redirects (302)", res.status_code == 302)

    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{total} CHECKS PASSED")
    print("=" * 60)

    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
