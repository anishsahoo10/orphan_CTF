import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DATABASE_DIR / "orphan.db")))

# System & Organization Meta (Apex Aeronautics // Project Apex Horizon)
APP_NAME = "APEX AERONAUTICS"
ORG_NAME = "APEX AERONAUTICS // SPECIAL PROJECTS GROUP"
NODE_ID = "APX-NODE-01"
NODE_LOCATION = "SITE BRAVO // OFFSHORE SUBTERRANEAN TEST RANGE"
SYSTEM_STATUS = "RESTRICTED TEST TELEMETRY"
ADMINISTRATOR = "D. MERCER (LEAD AVIONICS ENGINEER)"
DOCUMENTATION_STATUS = "DEFENSE PROCUREMENT AUDIT // UNCATALOGUED LEAK"
LAST_MAINTENANCE = "2024-10-27"
LAST_SYSTEM_UPDATE = "ACTIVE TELEMETRY"

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
SECRET_KEY = os.getenv("SECRET_KEY", "apex-horizon-flight-key-8899ac")
SESSION_COOKIE_NAME = "apx_session"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
