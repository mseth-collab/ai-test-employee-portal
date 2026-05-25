"""Run dashboard: python -m software_org_ai_platform"""
import sys
import threading
import time
import webbrowser
import uvicorn

from software_org_ai_platform.settings import BASE_URL, PORT


def _open():
    time.sleep(1.2)
    webbrowser.open(BASE_URL)


if __name__ == "__main__":
    print("\n  Software Org AI Platform")
    print("  -------------------------")
    print(f"  {BASE_URL}")
    print("  Press Ctrl+C to stop.\n")
    sys.stdout.flush()
    threading.Thread(target=_open, daemon=True).start()
    uvicorn.run(
        "software_org_ai_platform.app:app",
        host="127.0.0.1",
        port=PORT,
        reload=False,
    )
