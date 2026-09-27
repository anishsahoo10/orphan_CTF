import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DATABASE_DIR / "orphan.db")))

# System & Fictional Meta
APP_NAME = "ORPHAN"
ORG_NAME = "Strong Coffee (LEGACY TELECOM)"
NODE_ID = "SCF-NODE-07"
NODE_LOCATION = "SECTOR-B / RACK-04 (LEGACY TELECOM VAULT)"
SYSTEM_STATUS = "ACTIVE"
ADMINISTRATOR = "UNREGISTERED"
DOCUMENTATION_STATUS = "ARCHIVED"
LAST_MAINTENANCE = "UNKNOWN"
LAST_SYSTEM_UPDATE = "UNKNOWN"

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
SECRET_KEY = os.getenv("SECRET_KEY", "scf-node07-session-secret-994c2e6f1a8b")
SESSION_COOKIE_NAME = "scf_session"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
