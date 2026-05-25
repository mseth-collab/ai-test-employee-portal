"""
Healthcare Clinic Bot - Web API
Run: python -m healthcare_clinic_bot  (port 8001 by default, opens browser)
Or:  uvicorn healthcare_clinic_bot.app:app --host 127.0.0.1 --port 8001
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path

from healthcare_clinic_bot.bot import handle_message, Session

app = FastAPI(
    title="Healthcare Clinic Bot",
    description="Simple bot for appointments, hours, location, and FAQs.",
    version="1.0.0",
)

# In-memory sessions (use a real store in production)
sessions: dict[str, Session] = {}


def get_or_create_session(session_id: str) -> Session:
    if session_id not in sessions:
        sessions[session_id] = Session()
    return sessions[session_id]


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.get("/", response_class=HTMLResponse)
def index():
    """Serve the chat UI."""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="<p>Chat UI not found. Put index.html in healthcare_clinic_bot/static/</p>",
        status_code=404,
    )


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Process a user message and return the bot reply."""
    session = get_or_create_session(req.session_id)
    reply, updated = handle_message(req.message, session)
    sessions[req.session_id] = updated
    return ChatResponse(reply=reply, session_id=req.session_id)


@app.get("/health")
def health():
    return {"status": "ok"}
