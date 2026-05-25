"""
from __future__ import annotations

# BestFrAIend — employee self-service assistant.
Searches HR, Confluence, Finance, Expense, and Education policies without human escalation.
"""

import re
from dataclasses import dataclass, field

from bestfraiend.faqs import match_faq
from bestfraiend.knowledge.data import SOURCE_LABELS
from bestfraiend.org_feed import get_org_feed, search_org_feed
from bestfraiend.search import list_sources, search


@dataclass
class Session:
    last_category: str | None = None
    last_doc_ids: list[str] = field(default_factory=list)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _match_any(text: str, *phrases: str) -> bool:
    t = text.lower()
    return any(p in t for p in phrases)


def _format_hit(doc, rank: int) -> str:
    return (
        f"**{doc.title}** ({doc.source})\n"
        f"{doc.content[:420]}{'…' if len(doc.content) > 420 else ''}\n"
        f"_Ref: {doc.id}_"
    )


def _is_org_feed_query(lower: str) -> bool:
    return _match_any(
        lower,
        "event", "all-hands", "hackathon", "enrollment", "office hours", "tech summit",
        "news", "announcement", "headline", "company update", "tech news",
        "stream", "live stream", "broadcast", "watching",
        "job", "jobs", "opening", "openings", "career", "hiring", "internal role",
        "what's on", "whats on", "this week", "upcoming", "ongoing",
    )


def handle_message(message: str, session: Session) -> tuple[str, Session]:
    msg = _normalize(message)
    lower = msg.lower()

    if not msg:
        return ("What would you like to know? Try PTO, expenses, tuition, or deployment runbooks.", session)

    # Greeting / help
    if _match_any(lower, "hi", "hello", "hey", "good morning", "good afternoon"):
        sources = list_sources()
        lines = [f"• **{s['label']}** ({s['count']} topics)" for s in sources]
        return (
            "Hi! I'm **BestFrAIend**, your employee assistant. I search company policies and internal docs "
            "so you don't have to chase HR, Finance, or IT.\n\n"
            "I can help with:\n" + "\n".join(lines) + "\n\n"
            "I also show **events, news, live streams, and internal jobs** in the side panel.\n\n"
            "Ask anything—e.g. *How much PTO do I get?*, *Any internal jobs in platform?*, *What's live today?*",
            session,
        )

    if _match_any(lower, "help", "what can you", "sources", "what do you know"):
        sources = list_sources()
        lines = [f"• {s['label']}: {s['count']} documents" for s in sources]
        return (
            "**BestFrAIend** searches these sources (synthetic demo data):\n"
            + "\n".join(lines)
            + "\n\nI also answer **events, news, streams, and internal jobs**—check the side panel or ask e.g. *upcoming events*.",
            session,
        )

    # FAQ exact match — fastest path, deterministic answers
    faq = match_faq(msg)
    if faq:
        return (
            faq.answer + "\n\n_This is a frequently answered question. Ask a follow-up if you need more detail._",
            session,
        )

    # Org feed: events, news, streams, internal jobs
    if _is_org_feed_query(lower):
        feed_hits = search_org_feed(msg)
        if feed_hits:
            return (
                "From the **org feed** (also on your side panel):\n\n"
                + "\n\n".join(feed_hits)
                + "\n\n_Open the side panel for the full list of ongoing & upcoming items._",
                session,
            )

    # Optional category filter (specific before broad)
    category = session.last_category
    if _match_any(lower, "onboard", "new hire", "day 1", "first day", "buddy", "probation", "30-60-90", "equipment setup"):
        category = "onboarding"
    elif _match_any(lower, "tax", "w-4", "w-2", "t4", "td1", "paye", "lohnsteuer", "withholding", "payroll", "p60", "hmrc", "steuer", "rsu equity tax", "year-end tax"):
        category = "tax"
    elif _match_any(lower, "401k", "pension", "rrsp", "benefit", "medical", "dental", "hsa", "fsa", "open enrollment", "health plan"):
        category = "benefits"
    elif _match_any(lower, "mfa", "password reset", "sso", "vpn", "phishing", "security training", "acceptable use"):
        category = "it"
    elif _match_any(lower, "tuition", "learning stipend", "certification", "conference attendance", "l&d", "learning and development"):
        category = "education"
    elif _match_any(lower, "hr ", " hr", "people ops", "leave", "pto", "parental", "remote work", "conduct"):
        category = "hr"
    elif _match_any(lower, "confluence", "wiki", "runbook", "deploy", "api catalog"):
        category = "confluence"
    elif _match_any(lower, "finance", "budget", "vendor", "cost center", "corporate card"):
        category = "finance"
    elif _match_any(lower, "expense", "travel", "receipt", "per diem", "reimburs", "client meal", "t&e"):
        category = "expense"
    elif _match_any(lower, "education", "training", "stipend"):
        category = "education"

    # Explicit source filter commands
    for cat, label in SOURCE_LABELS.items():
        if lower.startswith(f"search {cat}") or lower.startswith(f"in {cat}"):
            query = re.sub(rf"^(search|in)\s+{cat}\s*", "", lower, flags=re.I).strip() or msg
            hits = search(query, category=cat, top_k=2)
            session.last_category = cat
            session.last_doc_ids = [h.doc.id for h in hits]
            if not hits:
                return (f"No matches in **{label}** for that query. Try different keywords.", session)
            parts = [_format_hit(h.doc, i + 1) for i, h in enumerate(hits)]
            return (
                f"From **{label}**:\n\n" + "\n\n".join(parts) + "\n\n_Need more detail? Ask a follow-up._",
                session,
            )

    hits = search(msg, category=category, top_k=3)
    session.last_category = category
    session.last_doc_ids = [h.doc.id for h in hits]

    feed_hits = search_org_feed(msg) if _is_org_feed_query(lower) else []

    if not hits and feed_hits:
        return (
            "From the **org feed**:\n\n" + "\n\n".join(feed_hits),
            session,
        )

    if not hits:
        return (
            "I couldn't find a strong match in HR, Confluence, Finance, Expenses, or Education docs.\n\n"
            "Try: *PTO carryover*, *expense receipt*, *internal jobs*, *upcoming events*, *live streams*, or **help**.",
            session,
        )

    intro = "Here's what I found—you shouldn't need to email anyone for this:"
    if category:
        intro = f"From **{SOURCE_LABELS.get(category, category)}** — {intro.lower()}"

    parts = [_format_hit(h.doc, i + 1) for i, h in enumerate(hits)]
    body = intro + "\n\n" + "\n\n".join(parts)
    if feed_hits:
        body += "\n\n**Also from org feed:**\n" + "\n".join(feed_hits[:2])
    return body + "\n\n_Ask a follow-up or check the side panel for events & jobs._", session
