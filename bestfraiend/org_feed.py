"""
Synthetic org feed: events, news, streaming, internal jobs.
Demo data for BestFrAIend side panel and bot answers.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrgEvent:
    id: str
    title: str
    when: str
    where: str
    status: str  # ongoing | upcoming
    description: str


@dataclass(frozen=True)
class OrgNews:
    id: str
    headline: str
    published: str
    summary: str
    tag: str


@dataclass(frozen=True)
class OrgStream:
    id: str
    title: str
    status: str  # live | scheduled
    when: str
    channel: str
    viewers: int | None = None


@dataclass(frozen=True)
class AINewsItem:
    id: str
    title: str
    company: str
    summary: str
    published: str
    category: str   # model | product | research | industry


@dataclass(frozen=True)
class InternalJob:
    id: str
    title: str
    team: str
    location: str
    type: str  # full-time, contract, etc.
    posted: str


ONGOING_EVENTS: list[OrgEvent] = [
    OrgEvent(
        id="evt-001",
        title="Q1 All-Hands Week",
        when="Mon–Fri this week · 10:00 local",
        where="Zoom + Town Hall A (SF)",
        status="ongoing",
        description="Daily leadership updates, product demos, and AMA sessions. Recordings on intranet within 24h.",
    ),
    OrgEvent(
        id="evt-002",
        title="Hackathon: AI for Employees",
        when="Day 2 of 3 · until 6 PM today",
        where="Slack #hackathon-ai + Labs floor",
        status="ongoing",
        description="Build internal tools with the new org AI platform. Prizes for best employee-facing assistant.",
    ),
    OrgEvent(
        id="evt-004",
        title="March New Hire Onboarding Cohort",
        when="Week 2 · daily sessions 09:00 UTC",
        where="Zoom · Onboarding Hub",
        status="ongoing",
        description="Day 1–5 curriculum: culture, tools, security, benefits overview, and regional tax briefing (NA/EU tracks).",
    ),
    OrgEvent(
        id="evt-005",
        title="US Tax Season Support Hours",
        when="Mon–Fri · 12:00–14:00 ET",
        where="HR Slack #tax-help + Zoom drop-in",
        status="ongoing",
        description="Payroll team answers W-2, W-4, and RSU questions. Not personal tax advice.",
    ),
]

UPCOMING_EVENTS: list[OrgEvent] = [
    OrgEvent(
        id="evt-101",
        title="Engineering Tech Talk: Platform Reliability",
        when="Thu, Mar 12 · 16:00 UTC",
        where="Zoom (link in calendar)",
        status="upcoming",
        description="SRE team shares incident learnings and new runbook standards.",
    ),
    OrgEvent(
        id="evt-102",
        title="New Hire Welcome Social",
        when="Fri, Mar 14 · 17:00 local",
        where="Cafeteria + virtual",
        status="upcoming",
        description="Meet March cohort. RSVP in calendar invite.",
    ),
    OrgEvent(
        id="evt-103",
        title="Security Awareness Month Kickoff",
        when="Mon, Mar 17 · 09:00 UTC",
        where="Company-wide stream",
        status="upcoming",
        description="Mandatory 15-min briefing; phishing sim starts same week.",
    ),
    OrgEvent(
        id="evt-105",
        title="EU Payroll & Tax Workshop",
        when="Tue, Mar 18 · 11:00 CET",
        where="Zoom · UK & DE tracks",
        status="upcoming",
        description="PAYE, Lohnsteuer, and cross-border remote work—mandatory for new EU hires this quarter.",
    ),
    OrgEvent(
        id="evt-106",
        title="Onboarding Buddy Training",
        when="Wed, Mar 20 · 15:00 UTC",
        where="LMS live session",
        status="upcoming",
        description="How to support new hires in their first 90 days. Volunteer buddies welcome.",
    ),
    OrgEvent(
        id="evt-107",
        title="Tech Summit: Internal AI & Platform",
        when="Thu, Mar 27 · all day",
        where="Hybrid · SF + stream",
        status="upcoming",
        description="BestFrAIend, data mesh, and cloud migration roadmap. Keynotes streamed company-wide.",
    ),
]

ORG_NEWS: list[OrgNews] = [
    OrgNews(
        id="news-001",
        headline="BestFrAIend rolls out to all employees",
        published="Today",
        summary="Self-service answers across HR, Finance, Confluence, and L&D—no more waiting on email threads.",
        tag="Product",
    ),
    OrgNews(
        id="news-002",
        headline="Record customer NPS in Q4",
        published="Yesterday",
        summary="Company-wide thank-you: extra wellness day added to calendars in April.",
        tag="Company",
    ),
    OrgNews(
        id="news-003",
        headline="New hybrid office policy refresh",
        published="Mar 3",
        summary="Updated guidance on in-office days and international remote—see HR portal.",
        tag="HR",
    ),
    OrgNews(
        id="news-005",
        headline="GPT-assisted code review pilot in GitHub Enterprise",
        published="Today",
        summary="Platform team rolling out optional AI review comments—opt in via team settings.",
        tag="Tech",
    ),
    OrgNews(
        id="news-006",
        headline="Kubernetes 1.29 cluster upgrade complete",
        published="Yesterday",
        summary="All production workloads migrated; see runbook for deprecated API removals.",
        tag="Tech",
    ),
    OrgNews(
        id="news-007",
        headline="New hire onboarding portal refresh",
        published="Mar 5",
        summary="Unified Day 1 checklist, regional tax guides, and buddy matching in one hub.",
        tag="Onboarding",
    ),
    OrgNews(
        id="news-008",
        headline="2025 tax document calendar published",
        published="Mar 4",
        summary="W-2, T4, P60, and DE Lohnsteuerbescheinigung dates confirmed in Payroll wiki.",
        tag="Tax",
    ),
    OrgNews(
        id="news-009",
        headline="Zero-trust VPN rollout — phase 2",
        published="Mar 2",
        summary="EMEA offices move to new client by Mar 15; IT drop-in sessions all week.",
        tag="Tech",
    ),
    OrgNews(
        id="news-010",
        headline="Internal mobility program expansion",
        published="Feb 28",
        summary="6-month minimum in role before transfer; priority for high-demand skills areas.",
        tag="HR",
    ),
]

STREAMS: list[OrgStream] = [
    OrgStream(
        id="str-001",
        title="All-Hands Live: CEO Update",
        status="live",
        when="Now",
        channel="intranet/stream/all-hands",
        viewers=1842,
    ),
    OrgStream(
        id="str-002",
        title="Hackathon Demo Stage",
        status="live",
        when="Now",
        channel="intranet/stream/hackathon",
        viewers=312,
    ),
    OrgStream(
        id="str-004",
        title="Tech Summit Keynote (preview)",
        status="scheduled",
        when="Thu, Mar 27 · 09:00 UTC",
        channel="intranet/stream/tech-summit",
        viewers=None,
    ),
    OrgStream(
        id="str-005",
        title="Onboarding Welcome: March Cohort",
        status="scheduled",
        when="Daily · 09:00 UTC",
        channel="intranet/stream/onboarding",
        viewers=None,
    ),
]

AI_NEWS: list[AINewsItem] = [
    AINewsItem(
        id="ai-001",
        title="OpenAI launches GPT-5 with native reasoning chains",
        company="OpenAI",
        summary="GPT-5 ships multi-step chain-of-thought, 128K context, and improved code generation. Generally available via API and ChatGPT.",
        published="May 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-002",
        title="Google DeepMind releases Gemini 2.5 Ultra",
        company="Google DeepMind",
        summary="Gemini 2.5 Ultra tops benchmarks in coding, math, and multimodal reasoning. Native video understanding now included.",
        published="May 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-003",
        title="Anthropic ships Claude 4 with 500K-token context",
        company="Anthropic",
        summary="Claude 4 introduces Constitutional AI v2, improved tool use, and expanded 500K context window for enterprise workflows.",
        published="Apr 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-004",
        title="Meta releases Llama 4 open-source model family",
        company="Meta AI",
        summary="Llama 4 includes dense and MoE variants. All weights available on Hugging Face. Supports up to 128K context.",
        published="Apr 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-005",
        title="Microsoft Copilot gets multi-agent autonomous workflows",
        company="Microsoft",
        summary="Copilot Studio adds agent orchestration — automated end-to-end business workflows without human-in-the-loop steps.",
        published="May 2026",
        category="product",
    ),
    AINewsItem(
        id="ai-006",
        title="AI coding tools now power 35% of enterprise code",
        company="GitHub / Industry",
        summary="GitHub's 2026 developer report: Copilot, Cursor, and Windsurf collectively write over a third of new code at Fortune 500s.",
        published="May 2026",
        category="industry",
    ),
    AINewsItem(
        id="ai-007",
        title="xAI's Grok 3 enters enterprise market",
        company="xAI",
        summary="Grok 3 launches with an enterprise tier, on-prem deployment options, and claimed 20% faster inference than GPT-4o.",
        published="Apr 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-008",
        title="12 AI leaders form agentic AI standards working group",
        company="Industry Coalition",
        summary="OpenAI, Google, Anthropic, Microsoft, Meta and 7 others form a body to define agent safety, interoperability, and audit standards.",
        published="May 2026",
        category="industry",
    ),
    AINewsItem(
        id="ai-009",
        title="Mistral AI releases Mistral Large 3 for enterprises",
        company="Mistral AI",
        summary="Mistral Large 3 targets European enterprise compliance, with GDPR-first data residency options and strong multilingual support.",
        published="May 2026",
        category="model",
    ),
    AINewsItem(
        id="ai-010",
        title="AI agent benchmarks show 60% task completion on real-world work",
        company="Stanford HAI",
        summary="Stanford's 2026 AI Index: agents now complete 60% of simulated enterprise tasks end-to-end, up from 22% in 2024.",
        published="May 2026",
        category="research",
    ),
]

INTERNAL_JOBS: list[InternalJob] = [
    InternalJob(
        id="job-001",
        title="Senior Software Engineer, Platform",
        team="Infrastructure",
        location="Remote · AMER",
        type="Full-time",
        posted="2 days ago",
    ),
    InternalJob(
        id="job-002",
        title="Product Manager, Employee Experience",
        team="People Products",
        location="Hybrid · London",
        type="Full-time",
        posted="4 days ago",
    ),
    InternalJob(
        id="job-003",
        title="Data Analyst, Finance Ops",
        team="FP&A",
        location="Remote · Global",
        type="Full-time",
        posted="1 week ago",
    ),
    InternalJob(
        id="job-004",
        title="Technical Writer, Developer Docs",
        team="Developer Relations",
        location="Remote · EMEA",
        type="Full-time",
        posted="1 week ago",
    ),
    InternalJob(
        id="job-006",
        title="Payroll Specialist (US/Canada)",
        team="Global Payroll",
        location="Remote · North America",
        type="Full-time",
        posted="1 day ago",
    ),
    InternalJob(
        id="job-007",
        title="Staff Engineer, AI Platform",
        team="BestFrAIend / Search",
        location="Hybrid · Seattle",
        type="Full-time",
        posted="2 days ago",
    ),
    InternalJob(
        id="job-008",
        title="Onboarding Program Manager",
        team="People Operations",
        location="Hybrid · Dublin",
        type="Full-time",
        posted="5 days ago",
    ),
    InternalJob(
        id="job-009",
        title="Security Engineer, Zero Trust",
        team="IT Security",
        location="Remote · EMEA",
        type="Full-time",
        posted="1 week ago",
    ),
    InternalJob(
        id="job-010",
        title="Benefits Analyst",
        team="Total Rewards",
        location="Hybrid · Toronto",
        type="Full-time",
        posted="6 days ago",
    ),
]


def get_org_feed() -> dict:
    """Full payload for side panel and portal views."""
    tech_news = [n for n in ORG_NEWS if n.tag == "Tech"]
    company_news = [n for n in ORG_NEWS if n.tag != "Tech"]
    return {
        "ongoing_events": [_event_dict(e) for e in ONGOING_EVENTS],
        "upcoming_events": [_event_dict(e) for e in UPCOMING_EVENTS],
        "news": [_news_dict(n) for n in ORG_NEWS],
        "company_news": [_news_dict(n) for n in company_news],
        "tech_news": [_news_dict(n) for n in tech_news],
        "streams": [_stream_dict(s) for s in STREAMS],
        "internal_jobs": [_job_dict(j) for j in INTERNAL_JOBS],
        "ai_news": [_ai_news_dict(n) for n in AI_NEWS],
    }


def _event_dict(e: OrgEvent) -> dict:
    return {
        "id": e.id,
        "title": e.title,
        "when": e.when,
        "where": e.where,
        "status": e.status,
        "description": e.description,
    }


def _news_dict(n: OrgNews) -> dict:
    return {"id": n.id, "headline": n.headline, "published": n.published, "summary": n.summary, "tag": n.tag}


def _stream_dict(s: OrgStream) -> dict:
    d = {"id": s.id, "title": s.title, "status": s.status, "when": s.when, "channel": s.channel}
    if s.viewers is not None:
        d["viewers"] = s.viewers
    return d


def _ai_news_dict(n: AINewsItem) -> dict:
    return {"id": n.id, "title": n.title, "company": n.company, "summary": n.summary, "published": n.published, "category": n.category}


def _job_dict(j: InternalJob) -> dict:
    return {
        "id": j.id,
        "title": j.title,
        "team": j.team,
        "location": j.location,
        "type": j.type,
        "posted": j.posted,
    }


def search_org_feed(query: str) -> list[str]:
    """Return formatted snippets matching events, news, streams, or jobs."""
    q = query.lower()
    results: list[str] = []

    for e in ONGOING_EVENTS + UPCOMING_EVENTS:
        blob = f"{e.title} {e.description} {e.where}".lower()
        if any(w in blob for w in q.split() if len(w) > 2):
            label = "Ongoing" if e.status == "ongoing" else "Upcoming"
            results.append(f"**{label}: {e.title}** — {e.when} · {e.where}\n{e.description}")

    for n in ORG_NEWS:
        blob = f"{n.headline} {n.summary} {n.tag}".lower()
        if any(w in blob for w in q.split() if len(w) > 2) or ("tech" in q and n.tag == "Tech"):
            results.append(f"**News: {n.headline}** ({n.published}) [{n.tag}]\n{n.summary}")

    for s in STREAMS:
        blob = f"{s.title} {s.channel}".lower()
        if any(w in blob for w in q.split() if len(w) > 2) or "stream" in q or "live" in q:
            live = "🔴 LIVE" if s.status == "live" else "Scheduled"
            extra = f" · {s.viewers} watching" if s.viewers else ""
            results.append(f"**Stream: {s.title}** [{live}]{extra}\n{s.when} · {s.channel}")

    for j in INTERNAL_JOBS:
        blob = f"{j.title} {j.team} {j.location}".lower()
        if any(w in blob for w in q.split() if len(w) > 2) or "job" in q or "role" in q or "opening" in q:
            results.append(f"**Job: {j.title}** — {j.team} · {j.location} ({j.type}, posted {j.posted})")

    return results[:4]
