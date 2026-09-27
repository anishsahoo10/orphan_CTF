"""Database initialization and seeding script for ORPHAN - Strong Coffee (LEGACY TELECOM)."""
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

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    clearance_level TEXT NOT NULL,
    status TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    classification TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    created_date TEXT NOT NULL,
    author TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    last_check TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    details TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flag_name TEXT UNIQUE NOT NULL,
    flag_value TEXT NOT NULL,
    description TEXT NOT NULL
);
"""


def init_database(db_path: Path = DATABASE_PATH, force_recreate: bool = False):
    """Create database tables and seed baseline fictional data."""
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
    """Seed initial fictional records for Strong Coffee (LEGACY TELECOM)."""
    cursor = conn.cursor()

    print("[*] Seeding database with baseline records...")

    # 1. Users (d.mercer password set to 'telecom2019' for rockyou.txt crackability)
    users = [
        (
            "operator",
            hash_password("AxiomLegacy2019!"),
            "operator",
            "2018-03-01 08:00:00",
            "2019-03-14 17:42:19",
        ),
        (
            "d.mercer",
            hash_password("telecom2019"),
            "sysadmin",
            "2018-02-14 09:30:00",
            "2019-02-28 11:20:04",
        ),
        (
            "legacy_service",
            hash_password("Svc_Node07_B78a11"),
            "system",
            "2018-03-01 08:05:00",
            "2019-03-15 00:00:00",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO users (username, password_hash, role, created_at, last_login)
        VALUES (?, ?, ?, ?, ?)
        """,
        users,
    )

    # 2. Employees
    employees = [
        (
            "SCF-0194",
            "Daniel Mercer",
            "Core Telecom Infrastructure",
            "LEVEL-3",
            "ARCHIVED / SEPARATED",
            "d.mercer@strongcoffee.internal",
        ),
        (
            "SCF-0248",
            "Iris Caldwell",
            "Fiber Routing & PBX Ops",
            "LEVEL-2",
            "DEPARTED",
            "i.caldwell@strongcoffee.internal",
        ),
        (
            "SCF-0312",
            "Nathan Cole",
            "Switchboard Database Administration",
            "LEVEL-2",
            "TRANSFERRED",
            "n.cole@strongcoffee.internal",
        ),
        (
            "SCF-0409",
            "Maya Rowan",
            "Telecom Infrastructure Auditing",
            "LEVEL-1",
            "INACTIVE",
            "m.rowan@strongcoffee.internal",
        ),
        (
            "SCF-0110",
            "Victor Vance",
            "Director of Legacy Telecom Operations",
            "LEVEL-4",
            "ARCHIVED",
            "v.vance@strongcoffee.internal",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO employees (employee_id, name, department, clearance_level, status, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        employees,
    )

    # 3. Documents
    documents = [
        (
            "system-overview",
            "System Architecture - Node SCF-07",
            "INTERNAL USE ONLY",
            "TELECOM",
            """NODE SPECIFICATION: SCF-NODE-07
ORGANIZATION: STRONG COFFEE (LEGACY TELECOM)
ROLE: AUXILIARY STAGING / ARCHIVAL ROUTER
ORIGIN DATE: 2018-04-12
CUSTODIAN: DANIEL MERCER (CORE TELECOM INFRASTRUCTURE)

PURPOSE:
SCF-NODE-07 was provisioned during the Phase 2 Core Migration project to function as an isolated archival bridge and intermediate data warehouse for legacy telecommunications routing tables and circuit logs. It was intended to host legacy department records, temporary database replicas, and internal documentation while primary assets moved to cloud infrastructure.

DECOMMISSION DIRECTIVE:
According to Migration Order MO-2018-99, this node was designated as temporary staging hardware. Target decommissioning was set for Q4 2018 following the validation of central directory synchronization.

STATUS NOTE:
Central synchronization was canceled during the corporate restructuring of November 2018. Node remains active under local fallback configuration in the Sector B cage.""",
            "2018-04-12",
            "Daniel Mercer (SCF-0194)",
        ),
        (
            "maintenance-log",
            "Maintenance & Patch Log: Q3 2018 - Q1 2019",
            "RESTRICTED",
            "MAINTENANCE",
            """==================================================
STRONG COFFEE (LEGACY TELECOM) - MAINTENANCE RECORD
NODE: SCF-NODE-07
==================================================

[2018-07-11] - Iris Caldwell:
Applied kernel update 4.15.0-generic. Verified telecom packet throughput on primary fiber adapter.

[2018-10-04] - Iris Caldwell:
Scheduled patch cycle suspended. Directive from management: do not apply major package revisions to temporary migration nodes. All active telecom workloads to be migrated out by end of quarter.

[2018-12-15] - Daniel Mercer:
Local service daemon restart completed. System time clock synchronized against internal telecom NTP server.

[2019-02-19] - Iris Caldwell:
Decommission ticket SCF-8829 status: PENDING SIGN-OFF.
The server was scheduled for power-down on March 15, 2019. Department reorganization has dispersed the staging team. Reassigning ticket to general telecom infrastructure backlog.

[2019-03-14] - System Daemon:
Automated health check executed. 0 errors reported. Routine monitoring agent unreachable. Subsequent health check logs truncated.""",
            "2019-02-19",
            "Iris Caldwell (SCF-0248)",
        ),
        (
            "deployment-notes",
            "Node SCF-07 Initial Provisioning & Switchboard Binding",
            "INTERNAL USE ONLY",
            "TELECOM",
            """PROVISIONING MANIFEST
ORGANIZATION: STRONG COFFEE (LEGACY TELECOM)
HOSTNAME: scf-node-07.internal.strongcoffee
HARDWARE ID: SRV-R04-B12
PRIMARY OPERATING SYSTEM: Legacy Linux 64-bit

NETWORK BINDINGS:
- Local Host: 127.0.0.1
- Management Subnet Interface: 10.0.4.7
- Public Gateway: Disabled by policy

SERVICES CONFIGURED:
- WEB-NODE: Internal port 8000 (HTTP interface)
- DATABASE: SQLite standalone embedded storage
- AUTHENTICATION: Local shadow hash verification
- DOCUMENTATION: Static archival document store
- INTERNAL API: Telemetry and status endpoints

NOTES:
Local authentication database was initialized with standard staging operators. Single sign-on federation was deferred pending migration. No remote monitoring agents were registered in the corporate asset inventory.""",
            "2018-03-05",
            "Nathan Cole (SCF-0312)",
        ),
        (
            "network-reference",
            "Subnet Routing & Fiber Interface Directives",
            "RESTRICTED",
            "NETWORK",
            """NETWORK TOPOLOGY REFERENCE
NODE: SCF-NODE-07
LOCATION: RACK-04, SECTOR-B (DEPRECATED TELECOM VAULT)

INTERFACE DETAILS:
eth0: 10.0.4.7 / 255.255.255.0
Gateway: 10.0.4.1 (Static routes internal only)
DNS: 10.0.0.2, 10.0.0.3 (Unreachable since subnet split)

ROUTING CONSTRAINTS:
Inbound traffic is restricted to internal subnet ranges.
Direct Internet egress is physically decoupled at the border router.
Any host capable of reaching this node must reside within or bridge into the legacy corporate lab network.""",
            "2018-09-30",
            "Iris Caldwell (SCF-0248)",
        ),
        (
            "archived-notes",
            "Audit Note #409: Uncatalogued Telecom Asset Inquiries",
            "CONFIDENTIAL / SEALED",
            "MEMO",
            """MEMORANDUM
TO: Telecom Infrastructure Compliance Committee
FROM: Maya Rowan (SCF-0409, Infrastructure Auditing)
DATE: November 14, 2020
SUBJECT: Uncatalogued Asset Inquiries - Sector B Physical Audit

During the annual perimeter sweep, network monitoring identified persistent TCP traffic originating from IP address 10.0.4.7.

A physical inspection of the Sector B server room was conducted on November 12, 2020. A 2U rack server labeled 'SCF-07' with faded 'STRONG COFFEE TELECOM' stenciling was observed in Rack 04. The unit was powered on, cooling fans operational, and drive activity indicators showed periodic access.

Cross-referencing the serial tag against the active Enterprise Asset Management system returned:
RECORD_NOT_FOUND

HR records confirm that the personnel who originally requested the hardware allocation (Daniel Mercer, Iris Caldwell) are no longer with the organization following the 2019 departmental dissolution.

RECOMMENDATION:
Identify all services running on SCF-07 and schedule an orderly decommission during the 2021 audit cycle.

STATUS:
Archived without resolution. No follow-up ticket was submitted.""",
            "2020-11-14",
            "Maya Rowan (SCF-0409)",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO documents (slug, title, classification, category, content, created_date, author)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        documents,
    )

    # 4. System Services
    services = [
        ("WEB-NODE", "ACTIVE", "scf-http/1.4.2-legacy", "2019-03-14 02:11:00", "d.mercer"),
        ("DATABASE", "ACTIVE", "sqlite-embedded/3.x", "2019-03-14 02:11:00", "n.cole"),
        ("AUTHENTICATION", "ACTIVE", "scf-auth-local/2.1", "2019-03-14 02:11:00", "i.caldwell"),
        ("DOCUMENTATION", "ACTIVE", "scf-docstore/0.9b", "2019-03-14 02:11:00", "d.mercer"),
        ("INTERNAL API", "ACTIVE", "scf-api-gw/1.0", "2019-03-14 02:11:00", "n.cole"),
    ]
    cursor.executemany(
        """
        INSERT INTO system_services (name, status, version, last_check, owner)
        VALUES (?, ?, ?, ?, ?)
        """,
        services,
    )

    # 5. Audit Logs
    audit_logs = [
        ("2018-04-12 09:00:12", "SYSTEM_INIT", "127.0.0.1", "Node SCF-NODE-07 initialized by administrator d.mercer"),
        ("2018-07-11 14:22:45", "KERNEL_PATCH", "10.0.4.15", "Kernel patch 4.15.0 applied by operator i.caldwell"),
        ("2018-10-04 11:05:00", "POLICY_CHANGE", "10.0.1.2", "Automated patching disabled per directive MO-2018-99"),
        ("2019-02-19 16:48:30", "TICKET_UPDATE", "10.0.4.22", "Decommission ticket SCF-8829 reassigned to unassigned queue"),
        ("2019-03-14 17:42:19", "AUTH_LOGIN", "10.0.4.7", "User operator authenticated successfully via local terminal"),
        ("2019-03-15 00:00:00", "CRON_EXEC", "127.0.0.1", "Nightly routine log rotation completed. Archival agent deactivated."),
        ("2020-11-12 11:34:02", "NETWORK_PING", "10.0.8.4", "ICMP sweep detected from audit console"),
    ]
    cursor.executemany(
        """
        INSERT INTO audit_logs (timestamp, event_type, source_ip, details)
        VALUES (?, ?, ?, ?)
        """,
        audit_logs,
    )

    # 6. CTF System Flags (User Flag for SQLi extraction)
    flags = [
        (
            "USER_FLAG",
            "flag{str0ng_c0ff33_sql1_untr4ck3d_n0d3_994c}",
            "Initial foothold flag captured via database extraction",
        )
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
