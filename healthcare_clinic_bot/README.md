# Healthcare Clinic Bot

A simple chatbot for a healthcare clinic. It can:

- **Greet** and answer FAQs  
- **Hours** – clinic opening/closing times  
- **Location** – address and directions  
- **Appointments** – guided flow to request an appointment (name → reason → preferred day)  
- **Services** – list of offered services  
- **Emergency** – reminds to call 911 for emergencies  

## Run the web app

From the **project root** (`AI-SQLQuery Doctor`):

```bash
# Use existing venv if you have one
.venv\Scripts\activate   # Windows
# or: source .venv/bin/activate  # macOS/Linux

pip install -r healthcare_clinic_bot/requirements.txt

# Start server and open browser automatically:
python -m healthcare_clinic_bot

# Or start server only, then open the URL printed in the console:
uvicorn healthcare_clinic_bot.app:app --host 127.0.0.1 --port 8001 --reload
```

The chat UI is **http://127.0.0.1:8001** by default (port **8001** avoids clashing with other tools on 8000). A browser tab should open when you use `python -m healthcare_clinic_bot`. To use another port: `set CLINIC_BOT_PORT=8002` (Windows) then run again.

## Run in the terminal (CLI)

From the project root, with the same venv active:

```bash
python -m healthcare_clinic_bot.cli
```

Type your messages and press Enter. Type `quit` or `exit` to stop.

## Customize

Edit `healthcare_clinic_bot/bot.py` to change:

- `CLINIC_NAME`, `CLINIC_HOURS`, `CLINIC_ADDRESS`, `CLINIC_PHONE`, `SERVICES`  
- Keyword lists and reply text for each intent  
- The appointment flow (e.g. add email, time slot)
