"""Run BestFrAIend: python -m bestfraiend"""
import sys
import threading
import time
import webbrowser
import uvicorn

from bestfraiend.settings import BASE_URL, PORT


def _open():
    time.sleep(1.2)
    webbrowser.open(BASE_URL)


if __name__ == "__main__":
    print("\n  BestFrAIend")
    print("  -----------")
    print(f"  {BASE_URL}")
    print("  Employee knowledge assistant (HR, Confluence, Finance, Expense, Education)")
    print("  Press Ctrl+C to stop.\n")
    sys.stdout.flush()
    threading.Thread(target=_open, daemon=True).start()
    uvicorn.run("bestfraiend.app:app", host="127.0.0.1", port=PORT, reload=False)
