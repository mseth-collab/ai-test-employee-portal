"""
Run the clinic bot server and open the browser.
Usage: python -m healthcare_clinic_bot

Default port 8001 (change with env CLINIC_BOT_PORT) so 8000 can stay free for other apps.
"""
import sys
import threading
import time
import webbrowser
import uvicorn

from healthcare_clinic_bot.settings import BASE_URL, PORT


def _open_browser():
    time.sleep(1.4)
    webbrowser.open(BASE_URL)


if __name__ == "__main__":
    print("\n  Healthcare Clinic Bot")
    print("  --------------------")
    print(f"  URL:   {BASE_URL}")
    print("  If the browser does not open, copy the URL above into your browser.")
    print("  Press Ctrl+C to stop the server.\n")
    sys.stdout.flush()
    t = threading.Thread(target=_open_browser, daemon=True)
    t.start()
    try:
        uvicorn.run(
            "healthcare_clinic_bot.app:app",
            host="127.0.0.1",
            port=PORT,
            reload=False,
        )
    except OSError as e:
        if "10048" in str(e) or "address already in use" in str(e).lower() or "Only one usage" in str(e):
            print(f"\n  Port {PORT} is already in use. Try: set CLINIC_BOT_PORT=8002")
            print(f"  then run again, or close the other app using that port.\n")
        raise
