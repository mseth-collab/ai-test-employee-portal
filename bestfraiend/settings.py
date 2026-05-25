import os

PORT = int(os.environ.get("BESTFRAIEND_PORT", "8003"))
BASE_URL = f"http://127.0.0.1:{PORT}"
