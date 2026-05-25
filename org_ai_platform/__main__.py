"""Run the Org AI Platform and open the browser."""
import sys
import webbrowser
import threading
import time
import uvicorn

def _open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("\n  Org AI Platform")
    print("  ---------------")
    print("  Opening http://127.0.0.1:8000")
    print("  Press Ctrl+C to stop.\n")
    sys.stdout.flush()
    thread = threading.Thread(target=_open_browser)
    thread.daemon = True
    thread.start()
    uvicorn.run(
        "org_ai_platform.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
