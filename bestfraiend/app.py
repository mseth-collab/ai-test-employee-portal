"""
BestFrAIend web API.
Run: python -m bestfraiend
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from bestfraiend.bot import Session, handle_message
from bestfraiend.faqs import CATEGORY_LABELS, list_faqs_by_category
from bestfraiend.org_feed import get_org_feed
from bestfraiend.search import list_sources

app = FastAPI(
    title="BestFrAIend",
    description="Employee assistant — search HR, Confluence, Finance, Expense, Education policies.",
    version="1.0.0",
)

STATIC = Path(__file__).parent / "static"
sessions: dict[str, Session] = {}


def _session(sid: str) -> Session:
    if sid not in sessions:
        sessions[sid] = Session()
    return sessions[sid]


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.get("/", response_class=HTMLResponse)
def index():
    p = STATIC / "index.html"
    if p.exists():
        return HTMLResponse(p.read_text(encoding="utf-8"))
    return HTMLResponse("<p>Missing static/index.html</p>", status_code=404)


@app.get("/static/{path:path}")
def static_file(path: str):
    full = STATIC / path
    if full.is_file():
        return FileResponse(full)
    return HTMLResponse("Not found", status_code=404)


@app.get("/api/faqs")
def api_faqs():
    """All FAQs grouped by category for the FAQ view."""
    grouped = list_faqs_by_category()
    return {
        "categories": [
            {
                "id": cat,
                "label": CATEGORY_LABELS.get(cat, cat),
                "faqs": grouped[cat],
            }
            for cat in grouped
        ]
    }


@app.get("/api/sources")
def api_sources():
    return {"sources": list_sources(), "total_docs": sum(s["count"] for s in list_sources())}


@app.get("/api/org-feed")
def api_org_feed():
    """Side panel: events, news, streams, internal jobs."""
    return get_org_feed()


@app.get("/api/knowledge/{category}")
def knowledge_category(category: str):
    """Policy documents for a portal section (onboarding, tax, hr, etc.)."""
    from bestfraiend.knowledge.data import KNOWLEDGE_BASE, SOURCE_LABELS

    docs = [d for d in KNOWLEDGE_BASE if d.category == category]
    return {
        "category": category,
        "label": SOURCE_LABELS.get(category, category),
        "documents": [
            {
                "id": d.id,
                "title": d.title,
                "summary": d.summary,
                "source": d.source,
                "content": d.content,
            }
            for d in docs
        ],
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = _session(req.session_id)
    reply, updated = handle_message(req.message, session)
    sessions[req.session_id] = updated
    return ChatResponse(reply=reply, session_id=req.session_id)


@app.get("/health")
def health():
    return {"status": "ok", "name": "BestFrAIend"}
