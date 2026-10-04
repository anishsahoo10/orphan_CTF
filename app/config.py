import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DATABASE_DIR / "orphan.db")))

# System & Organization Meta
APP_NAME = "AETHELGARD"
ORG_NAME = "AETHELGARD HOLDINGS // ARCHIPELAGO ARCHIVES"
NODE_ID = "ATG-NODE-01"
NODE_LOCATION = "SITE BRAVO // PRIVATE HANGAR & ESTATE VAULT"
SYSTEM_STATUS = "RESTRICTED ACCESS"
ADMINISTRATOR = "H. VANCE (LOGISTICS & DISPATCH)"
DOCUMENTATION_STATUS = "UNREDACTED LEAK"
LAST_MAINTENANCE = "2024-10-27"
LAST_SYSTEM_UPDATE = "ACTIVE PERSISTENCE"

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
SECRET_KEY = os.getenv("SECRET_KEY", "aethelgard-secure-session-key-8899ac")
SESSION_COOKIE_NAME = "atg_session"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
