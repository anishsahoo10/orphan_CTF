"""Database initialization and seeding script for APEX AERONAUTICS (Project Apex Horizon)."""
import os
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import DATABASE_DIR, DATABASE_PATH
from app.utils.auth import hash_password


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'engineer',
    created_at TEXT NOT NULL,
    last_login TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    subject TEXT NOT NULL,
    classification TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT UNIQUE NOT NULL,
    tail_number TEXT NOT NULL,
    departure_hub TEXT NOT NULL,
    arrival_hub TEXT NOT NULL,
    flight_date TEXT NOT NULL,
    aircraft_model TEXT NOT NULL,
    passenger_count INTEGER NOT NULL,
    manifest_notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    coordinates TEXT NOT NULL,
    classification TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flag_name TEXT UNIQUE NOT NULL,
    flag_value TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    details TEXT NOT NULL
);
"""


def init_database(db_path: Path = DATABASE_PATH, force_recreate: bool = False):
    """Create database tables and seed baseline aerospace defense records."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    if force_recreate and db_path.exists():
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript(SCHEMA_SQL)

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_data(conn)
    else:
        print("[*] Database tables already populated.")

    conn.commit()
    conn.close()
    print(f"[+] Database initialized successfully at: {db_path}")


def seed_data(conn: sqlite3.Connection):
    """Seed initial aerospace defense records for Apex Aeronautics."""
    cursor = conn.cursor()

    print("[*] Seeding database with Apex Aeronautics project records...")

    # 1. Users (Retaining d.mercer and operator)
    users = [
        (
            "operator",
            hash_password("AxiomLegacy2019!"),
            "operator",
            "2023-01-10 08:00:00",
            "2024-10-27 19:42:19",
        ),
        (
            "d.mercer",
            hash_password("telecom2019"),
            "lead-avionics",
            "2022-11-14 09:30:00",
            "2024-10-25 11:20:04",
        ),
        (
            "h.vance",
            hash_password("telecom2019"),
            "flight-director",
            "2022-04-01 10:15:00",
            "2024-10-26 22:45:10",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO users (username, password_hash, role, created_at, last_login)
        VALUES (?, ?, ?, ?, ?)
        """,
        users,
    )

    # 2. Aerospace Test Correspondence (Mails / Logs)
    messages = [
        (
            "h.vance@apex-aero.internal",
            "flight-ops@apex-aero.internal",
            "2024-10-20 14:15:22",
            "TEST DIRECTIVE: Prototype Airframe APX-650 Test Window",
            "RESTRICTED // SPECIAL ACCESS",
            """FLIGHT TEST DIRECTIVE // EYES ONLY
Prototype airframe N708AG (Apex-650 Stealth Conversion) has completed pre-flight avionics burn-in at Subterranean Hangar 07. 

Departure is confirmed for 23:00 UTC with low-observable transit routing to Site Bravo Offshore Runway. Ground radar controllers must disable secondary transponders 50 nautical miles outside civil airspace per Protocol 9. No flight plans are to be filed with civil aviation authorities.

Verify subterranean arresting gear prior to touchdown.""",
        ),
        (
            "radar@apex-aero.internal",
            "d.mercer@apex-aero.internal",
            "2024-10-22 09:40:11",
            "TELEMETRY LOG: Radar Cross-Section Anomaly & Sea-Skimming Sweep",
            "CONFIDENTIAL // DEFENSE AUDIT",
            """RADAR TELEMETRY TRANSCRIPT // SITE BRAVO SENSOR ARRAY
TIME: 03:14 UTC
SENSOR: Coastal Phased Array (Array 04)
TARGET: Airframe N708AG

OBSERVATION:
Radar cross-section reduction of 84% confirmed during sea-skimming approach at 200 feet above sea level. Unregistered patrol craft detected 4 km off northern cove; tender intercepted without incident.

DIRECTIVE:
Increase thermal perimeter scan intervals. Maintain complete radio silence during night autonomous approach tests.""",
        ),
        (
            "dispatch@apex-aero.internal",
            "all-engineers@apex-aero.internal",
            "2024-10-24 18:22:05",
            "ENCRYPTED MEMO: Test Range Coordinates & Telemetry Relay Frequency",
            "TOP SECRET // COMPARTMENTED",
            """COORDINATES CONFIRMED:
Primary Island Compound: LAT 36.4523N, LON 28.1876E (Site Bravo - Mediterranean Basin)
Private Helipad Frequency: 122.85 MHz [Chirp ID: ECHO-7]

COMMUNICATIONS COMPLIANCE FLAG:
FLAG_4_COMMUNICATIONS: flag{pr1v4t3_m41l_c00rd1n4t3s_3xfl1tr4t3d_44b1}

Notice: All local mailbox archives are scheduled for automated cryptographic zeroing upon activation of emergency decommission protocol.""",
        ),
        (
            "compliance@apex-aero.internal",
            "d.mercer@apex-aero.internal",
            "2024-10-25 11:05:44",
            "COMPLIANCE AUDIT: Defense Procurement Inquiries Regarding Unlisted Airframes",
            "PRIVILEGED & CONFIDENTIAL",
            """Ministry of Defense auditors have formally requested maintenance logs for all modified Gulfstream airframes operated from Mediterranean staging hubs.

Do not retain digital backups of autonomous flight profiles on unencrypted workstations. Transfer all telemetry archives to isolated test node APX-NODE-01 immediately.""",
        ),
        (
            "sysadmin@apex-aero.internal",
            "d.mercer@apex-aero.internal",
            "2024-10-26 23:59:00",
            "CONFIDENTIAL IT DISPATCH // EMERGENCY ACCESS & CREDENTIALS",
            "TOP SECRET // RESTRICTED ACCESS",
            """EMERGENCY DISPATCH // EYES ONLY
Facility Node: ATG-NODE-01 (Site Bravo Staging Host)

FLAG 2: flag{sql1_3xtr4ct_v4nc3_cr3d3nt14ls_77d2}

SYSTEM OPERATOR CREDENTIALS:
Username: d.mercer
Password: telecom2019
Clearance: Lead Systems Architect / Logistics Director

INSTRUCTIONS FOR DISPATCH LEAD:
1. Use these credentials to sign in at the Executive Gateway (/login) to unlock the Classified Surveillance Vault (/photos).
2. Use these same credentials to establish an administrative SSH terminal on port 22 to inspect system daemons.""",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO messages (sender, recipient, timestamp, subject, classification, content)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        messages,
    )

    # 3. Prototype Flight Test Registry
    flights = [
        (
            "APX-701",
            "N708AG",
            "London Luton Special Ops (EGGW)",
            "Site Bravo Subterranean Runway (LGSB)",
            "2024-10-18",
            "Gulfstream G650ER (Apex Stealth Mod)",
            6,
            "Prototype autonomous flight control testing. Transponder deactivated per Defense Directive 14.",
        ),
        (
            "APX-704",
            "N708AG",
            "Istres-Le Tubé Flight Test Base (LFMI)",
            "Site Bravo Subterranean Runway (LGSB)",
            "2024-10-21",
            "Gulfstream G650ER (Apex Stealth Mod)",
            4,
            "Avionics sensor pod calibration. Uncatalogued optical telemetry package installed in forward fuselage.",
        ),
        (
            "APX-882",
            "N919AG",
            "Nice Côte d'Azur (LFMN)",
            "Site Bravo Helipad (SB-01)",
            "2024-10-23",
            "AgustaWestland AW139 (Tactical Tender)",
            3,
            "Tactical personnel transfer between offshore radar buoy and cliffside command bunker.",
        ),
        (
            "APX-910",
            "N708AG",
            "Dubai World Central (OMDW)",
            "Site Bravo Subterranean Runway (LGSB)",
            "2024-10-25",
            "Gulfstream G650ER (Apex Stealth Mod)",
            8,
            "Night autonomous approach test. Primary transponder killswitch engaged at Waypoint TITAN.",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO flights (flight_number, tail_number, departure_hub, arrival_hub, flight_date, aircraft_model, passenger_count, manifest_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        flights,
    )

    # 4. Classified Visual Reconnaissance (5 Photos)
    photos = [
        (
            "Site Bravo Offshore Test Facility & Subterranean Airfield",
            "AERIAL RECON",
            "/static/images/island_estate.jpg",
            "2024-10-27 18:45:00 UTC",
            "LAT 36.4523N, LON 28.1876E",
            "TOP SECRET",
            "High-altitude optical drone snapshot of the primary runway complex, cliffside command facility, and tactical helipad.",
        ),
        (
            "Flight Deck: Gulfstream N708AG Cockpit Avionics & Autopilot",
            "AVIONICS LOG",
            "/static/images/private_cockpit.jpg",
            "2024-10-25 21:14:00 UTC",
            "FL380 / TRANSIT WAYPOINT TITAN",
            "RESTRICTED",
            "Cockpit flight management display showing deactivated secondary transponder beacon prior to island descent.",
        ),
        (
            "Research Quarters: Site Bravo Coastal Command Center",
            "FACILITY INTERIOR",
            "/static/images/villa_interior.jpg",
            "2024-10-27 19:20:00 UTC",
            "MAIN COMPOUND / SECTOR 01",
            "CONFIDENTIAL",
            "Executive briefing lounge overlooking the northern maritime exclusion zone.",
        ),
        (
            "Subterranean Hangar 07: Prototype Airframe Staging",
            "AIRFIELD OPS",
            "/static/images/private_hangar.jpg",
            "2024-10-26 23:10:00 UTC",
            "SECURE RUNWAY ACCESS",
            "RESTRICTED",
            "Interior view of Hangar 07 staging airframe N708AG prior to midnight autonomous low-observable test run.",
        ),
        (
            "Coastal Radar Watch: Secluded Mooring & Radar Array CAM-05",
            "MARITIME RADAR",
            "/static/images/yacht_marina.jpg",
            "2024-10-27 01:34:58 UTC",
            "NORTHERN COVE DOCK",
            "CONFIDENTIAL",
            "Nightwatch camera feed CAM-5 capturing private yacht Nightstar docked at the secluded access pier. FLAG_5_MEDIA_VAULT: flag{cl4ss1f13d_fl1ght_m4n1f3st_v4ult_55f9}",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO photos (title, category, image_url, timestamp, coordinates, classification, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        photos,
    )

    # 5. CTF System Flags
    flags = [
        (
            "FLAG_1_RECON",
            "flag{4rch1p3l4g0_r3c0n_f1ng3rpr1nt_88a1}",
            "Flag 1: Initial host and HTTP response reconnaissance",
        ),
        (
            "FLAG_2_DATABASE",
            "flag{sql1_3xtr4ct_v4nc3_cr3d3nt14ls_77d2}",
            "Flag 2: SQL Injection database extraction & password hash discovery",
        ),
        (
            "FLAG_3_ROOT",
            "flag{r00t_m4st3r_4rch1p3l4g0_0wn3d_993c}",
            "Flag 3: Linux privilege escalation to root on the target VM",
        ),
        (
            "FLAG_4_COMMUNICATIONS",
            "flag{pr1v4t3_m41l_c00rd1n4t3s_3xfl1tr4t3d_44b1}",
            "Flag 4: Extraction of unredacted executive correspondence & island coordinates",
        ),
        (
            "FLAG_5_MEDIA_VAULT",
            "flag{cl4ss1f13d_fl1ght_m4n1f3st_v4ult_55f9}",
            "Flag 5: Access to the classified media vault and flight manifest records",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO system_flags (flag_name, flag_value, description)
        VALUES (?, ?, ?)
        """,
        flags,
    )


if __name__ == "__main__":
    force = "--reset" in sys.argv or "--force" in sys.argv
    init_database(force_recreate=force)
