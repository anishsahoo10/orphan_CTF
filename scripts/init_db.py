"""Database initialization and seeding script for AETHELGARD ARCHIVES (The Archipelago Network)."""
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
    role TEXT NOT NULL DEFAULT 'operator',
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
    """Create database tables and seed baseline investigative archive data."""
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
    """Seed initial investigative records for Aethelgard Holdings."""
    cursor = conn.cursor()

    print("[*] Seeding database with investigative leak records...")

    # 1. Users (Keeping d.mercer compatible with current VM setup, plus h.vance)
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
            "sysadmin",
            "2022-11-14 09:30:00",
            "2024-10-25 11:20:04",
        ),
        (
            "h.vance",
            hash_password("telecom2019"),
            "director",
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

    # 2. Executive Correspondence (Mails / Call Logs)
    messages = [
        (
            "h.vance@aethelgard.internal",
            "logistics@aethelgard.internal",
            "2024-10-20 14:15:22",
            "DISPATCH: Private Charter Schedule for Site Bravo",
            "RESTRICTED",
            """LOGISTICS MEMORANDUM // EYES ONLY
Flight N708AG has completed private pre-flight clearance at Hangar 07. Departure is confirmed for 23:00 UTC with direct routing to Site Bravo Private Runway. 

Ground personnel must disable transponders 30 nautical miles outside regional airspace as per Protocol 9. No local flight manifests are to be submitted to municipal aviation authorities.

Ensure the private guest pavilion is prepared prior to touchdown.""",
        ),
        (
            "security@aethelgard.internal",
            "h.vance@aethelgard.internal",
            "2024-10-22 09:40:11",
            "CALL LOG & INTERCEPT: Maritime Radar Ping Anomaly",
            "CONFIDENTIAL",
            """CALL TRANSCRIPT // RECORDED LINE 04
TIME: 03:14 UTC
CALLER: Watchpost Alpha (Harbor Master)
RECIPIENT: Chief Security Vance

TRANSCRIPT:
"Unregistered vessel entered perimeter waters 4 kilometers north of the private cove. Vessel was painted dark with navigation beacons extinguished. Our patrol tender intercepted and redirected the craft without incident. Vessel skipper claimed engine failure."

DIRECTIVE:
Increase thermal perimeter scan intervals on radar sweep. Do not permit unvetted vessels within 5 nautical miles of the island estate.""",
        ),
        (
            "dispatch@aethelgard.internal",
            "all-exec@aethelgard.internal",
            "2024-10-24 18:22:05",
            "ENCRYPTED MEMO: Estate Coordinates & Encrypted Archive Key",
            "TOP SECRET // COMPARTMENTED",
            """COORDINATES CONFIRMED:
Primary Island Compound: LAT 36.4523N, LON 28.1876E (Site Bravo - Mediterranean Basin)
Private Helipad Frequency: 122.85 MHz [Chirp ID: ECHO-7]

COMMUNICATIONS COMPLIANCE FLAG:
FLAG_4_COMMUNICATIONS: flag{pr1v4t3_m41l_c00rd1n4t3s_3xfl1tr4t3d_44b1}

Notice: All local mailbox archives are scheduled for automated cryptographic zeroing upon activation of emergency decommission protocol.""",
        ),
        (
            "legal@aethelgard.internal",
            "h.vance@aethelgard.internal",
            "2024-10-25 11:05:44",
            "LEGAL AUDIT: Subpoena Inquiries Regarding Offshore Holdings",
            "PRIVILEGED & CONFIDENTIAL",
            """Counsel confirms that the offshore trust records for Aethelgard Holdings remain physically sealed in the Panamanian registry. 

Do not retain digital backups of guest manifests or charter manifests on unencrypted workstations. Transfer all legacy data logs to the isolated staging node ATG-NODE-01 immediately.""",
        ),
        (
            "sysadmin@aethelgard.internal",
            "d.mercer@aethelgard.internal",
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

    # 3. Private Aviation Registry (Flights)
    flights = [
        (
            "ATG-701",
            "N708AG",
            "London Luton (EGGW)",
            "Site Bravo Private Runway (LGSB)",
            "2024-10-18",
            "Gulfstream G650ER",
            6,
            "VIP Private Charter. Customs clearance bypassed per Special Exemption Directive 14.",
        ),
        (
            "ATG-704",
            "N708AG",
            "Le Bourget Paris (LFPB)",
            "Site Bravo Private Runway (LGSB)",
            "2024-10-21",
            "Gulfstream G650ER",
            4,
            "Executive delegation. Unmanifested catering and secure diplomatic lockbox loaded in cargo bay.",
        ),
        (
            "ATG-882",
            "N919AG",
            "Nice Côte d'Azur (LFMN)",
            "Site Bravo Helipad (SB-01)",
            "2024-10-23",
            "AgustaWestland AW139",
            3,
            "Helicopter shuttle link between private marina and cliffside villa compound.",
        ),
        (
            "ATG-910",
            "N708AG",
            "Dubai World Central (OMDW)",
            "Site Bravo Private Runway (LGSB)",
            "2024-10-25",
            "Gulfstream G650ER",
            8,
            "Discreet passenger group. Transponder deactivated at Waypoint TITAN. Night landing verified.",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO flights (flight_number, tail_number, departure_hub, arrival_hub, flight_date, aircraft_model, passenger_count, manifest_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        flights,
    )

    # 4. Classified Media Vault (Photos & Surveillance Stills)
    photos = [
        (
            "SURVEILLANCE: Site Bravo Private Island Estate",
            "AERIAL RECON",
            "/static/images/island_estate.jpg",
            "2024-10-27 18:45:00 UTC",
            "LAT 36.4523N, LON 28.1876E",
            "TOP SECRET",
            "High-altitude optical drone snapshot of the main villa compound, private cliffside pathways, and tactical helipad. Coordinates verified.",
        ),
        (
            "HANGAR 07: Private Aviation Staging Facility",
            "AIRFIELD OPS",
            "/static/images/private_hangar.jpg",
            "2024-10-26 23:10:00 UTC",
            "SECURE RUNWAY ACCESS",
            "RESTRICTED",
            "Interior view of Hangar 07 hosting private jet N708AG prior to midnight departure. Maintenance and fueling logs archived.",
        ),
        (
            "PORT WATCH: Isolated Marina & Superyacht Mooring",
            "MARITIME RADAR",
            "/static/images/yacht_marina.jpg",
            "2024-10-27 01:34:58 UTC",
            "NORTHERN COVE DOCK",
            "CONFIDENTIAL",
            "Nightwatch camera feed CAM-5 capturing private yacht Nightstar docked at the secluded access pier. FLAG_5_MEDIA_VAULT: flag{cl4ss1f13d_fl1ght_m4n1f3st_v4ult_55f9}",
        ),
        (
            "FLIGHT DECK: Gulfstream N708AG Cockpit Avionics",
            "AVIONICS LOG",
            "/static/images/private_cockpit.jpg",
            "2024-10-25 21:14:00 UTC",
            "FL380 / TRANSIT WAYPOINT TITAN",
            "RESTRICTED",
            "Cockpit flight management display showing deactivated secondary transponder beacon prior to island descent.",
        ),
        (
            "RESIDENCE: Site Bravo Cliffside Lounge & Quarters",
            "ESTATE INTERIOR",
            "/static/images/villa_interior.jpg",
            "2024-10-27 19:20:00 UTC",
            "MAIN COMPOUND / SECTOR 01",
            "CONFIDENTIAL",
            "Interior architectural capture of executive lounge overlooking coastal waters. Private meeting sanctuary.",
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
