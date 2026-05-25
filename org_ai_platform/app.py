"""
Org-level AI Platform - Web app
Serves the dashboard and optional API stubs for Ask / Request.
Run: uvicorn org_ai_platform.app:app --reload
Or: python -m org_ai_platform (if __main__.py opens browser)
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="Org AI Platform",
    description="Enterprise assistant for HR, Finance, Ops, Tech, Grievance — 4000+ staff globally",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", response_class=HTMLResponse)
def index():
    """Serve the main dashboard."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<p>Static files not found.</p>", status_code=404)


@app.get("/static/{path:path}")
def static_file(path: str):
    """Serve CSS/JS etc. from static."""
    full = STATIC_DIR / path
    if full.is_file():
        return FileResponse(full)
    return HTMLResponse(content="Not found", status_code=404)


# Optional API stubs for integration
class AskRequest(BaseModel):
    department: str | None = None
    query: str


class AskResponse(BaseModel):
    answer: str
    department: str | None = None


@app.post("/api/ask", response_model=AskResponse)
def api_ask(req: AskRequest):
    """Stub: in production this would call your AI/orchestrator."""
    return AskResponse(
        answer="(Demo) Your question has been received. In production this would return an AI-generated answer based on department and policies.",
        department=req.department,
    )


class SubmitRequest(BaseModel):
    department: str
    category: str
    employee_id: str
    region: str | None = None
    subject: str
    description: str
    priority: str = "normal"


class SubmitResponse(BaseModel):
    ticket_id: str
    message: str


@app.post("/api/request", response_model=SubmitResponse)
def api_submit_request(req: SubmitRequest):
    """Stub: in production this would create a ticket and route to the right team."""
    import uuid
    ticket_id = f"{req.department.upper()}-{uuid.uuid4().hex[:8].upper()}"
    return SubmitResponse(
        ticket_id=ticket_id,
        message=f"Request submitted. Reference: {ticket_id}. You will be notified when it is processed.",
    )
