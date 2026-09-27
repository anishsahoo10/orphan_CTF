# ORPHAN // Strong Coffee (LEGACY TELECOM)

> *"It was never supposed to be there."*

A standalone internal web application representing a forgotten legacy telecommunications staging server discovered during an infrastructure security audit. Deployed under **Strong Coffee (LEGACY TELECOM)** as node `SCF-NODE-07`, this system serves as an unmaintained archival bridge with historical circuit logs, employee records, local subsystem monitors, and legacy console authentication.

---

## 1. Project Overview

`ORPHAN` is designed with an authentic, high-contrast, retro-modern dark web / abandoned telecom server visual identity. The interface emphasizes clean readability, spacious typography (`Plus Jakarta Sans` & `JetBrains Mono`), CCTV surveillance camera feeds, and narrative lore embedded into telecom logs and archival memos.

This repository represents the **development baseline** version. It implements standard, secure coding patterns (parameterized queries, bcrypt password hashing, and session authentication). Controlled attack vectors and CTF challenges will be layered on top of this modular architecture in subsequent stages.

---

## 2. Technology Stack

- **Backend**: Python 3.10+ / FastAPI / Starlette
- **Server**: Uvicorn ASGI
- **Templating**: Jinja2 (HTML5 / CSS3 / Vanilla JavaScript)
- **Database**: SQLite 3 (lightweight, zero external server dependencies)
- **Security Baseline**: `bcrypt` password hashing, signed HTTP-only cookies via `itsdangerous`

---

## 3. Project Structure

```text
orphan dev part/
├── app/
│   ├── __init__.py
│   ├── config.py             # System constants, host, port, paths, secret keys
│   ├── database.py           # SQLite connection pool and query helpers
│   ├── models.py             # Pydantic data schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Gateway (/), Status (/status), Docs (/documents), Dashboard (/dashboard)
│   │   ├── auth.py           # Login (/login), Logout (/logout)
│   │   └── api.py            # REST JSON endpoints (/api/status, /api/services, /api/documents)
│   └── utils/
│       ├── __init__.py
│       └── auth.py           # Bcrypt hashing and password verification
├── templates/
│   ├── base.html             # Two-column portal shell, CCTV surveillance widget, directory tree
│   ├── index.html            # Node gateway, hero photography, and 4-card status deck
│   ├── login.html            # Operator authentication console
│   ├── dashboard.html        # Historical employee directory, service matrix, and audit journal
│   ├── status.html           # Subsystem health grid and daemon telemetry
│   ├── documents.html        # Archival document repository index
│   ├── document_detail.html  # Plaintext archival document viewer with inspection evidence
│   └── error.html            # Themed diagnostic error display (NODE_UNAVAILABLE)
├── static/
│   ├── css/
│   │   └── style.css         # High-contrast retro-modern dark web portal styles
│   ├── js/
│   │   └── main.js           # Live UTC clock and CCTV timestamp synchronization
│   └── images/
│       ├── axiom-logo.svg    # Strong Coffee technical vector emblem
│       ├── strong_coffee_server.jpg # Server rack stenciled with "STRONG COFFEE TELECOM"
│       ├── coffee_console.jpg # Operator desk with CRT monitor & coffee mug
│       ├── cctv_rack.jpg     # Security camera still of Rack 04
│       └── facility_corridor.jpg # Sector B corridor still
├── database/
│   └── orphan.db             # Local SQLite database (seeded on init)
├── scripts/
│   ├── init_db.py            # Standalone database initialization and seed utility
│   └── test_app.py           # Automated test suite (47/47 checks passing)
├── requirements.txt          # Python package requirements
├── README.md                 # Project documentation
└── .gitignore                # Git exclusions
```

---

## 4. Development Setup

### Virtual Environment Setup

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS (Bash):**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 5. Dependency Installation

```bash
pip install -r requirements.txt
```

---

## 6. Database Initialization

The database automatically initializes upon app startup. You can also reseed manually:

```bash
python scripts/init_db.py --reset
```

### Baseline Accounts (Development Testing)
| Username | Role | Password | Description |
| :--- | :--- | :--- | :--- |
| `operator` | operator | `AxiomLegacy2019!` | Standard console operator |
| `d.mercer` | sysadmin | `Mercer#7f9a2b99` | Lead Telecom Architect (Separated) |

---

## 7. Running the Application

From the project root:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to: **`http://localhost:8000`**
