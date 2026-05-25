"""
Software org AI platform — dashboard with basic widgets.
Run: python -m software_org_ai_platform
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from software_org_ai_platform.settings import BASE_URL

app = FastAPI(
    title="Software Org AI Platform",
    description="Org AI dashboard for a software company (widgets, ask, stubs).",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", response_class=HTMLResponse)
def index():
    path = STATIC_DIR / "index.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(encoding="utf-8"))
    return HTMLResponse("<p>Missing static/index.html</p>", status_code=404)


@app.get("/static/{path:path}")
def static_file(path: str):
    full = STATIC_DIR / path
    if full.is_file():
        return FileResponse(full)
    return HTMLResponse("Not found", status_code=404)


class AskRequest(BaseModel):
    scope: str | None = None
    query: str


class AskResponse(BaseModel):
    answer: str
    scope: str | None = None


@app.post("/api/ask", response_model=AskResponse)
def api_ask(req: AskRequest):
    """Stub — replace with RAG / LLM + internal tools."""
    return AskResponse(
        answer=(
            "(Demo) In production, answers come from your knowledge graph, runbooks, "
            "and ticket APIs—scoped to Engineering / Product / People / IT as selected."
        ),
        scope=req.scope,
    )


@app.get("/health")
def health():
    return {"status": "ok", "demo_url": BASE_URL}
