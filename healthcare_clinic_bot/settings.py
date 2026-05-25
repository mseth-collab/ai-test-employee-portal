"""Server URL for the clinic bot (default 8001 — avoids conflict with typical apps on 8000)."""
import os

PORT = int(os.environ.get("CLINIC_BOT_PORT", "8001"))
BASE_URL = f"http://127.0.0.1:{PORT}"
