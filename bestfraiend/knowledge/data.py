"""
Synthetic employee knowledge base for BestFrAIend.
Sources: HR policies, Confluence wiki, Finance, Expenses, Education.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeDoc:
    id: str
    title: str
    source: str  # e.g. "HR Policy Portal", "Confluence"
    category: str  # hr | confluence | finance | expense | education
    summary: str
    content: str
    tags: tuple[str, ...]


KNOWLEDGE_BASE: list[KnowledgeDoc] = [
    # --- HR policies ---
    KnowledgeDoc(
        id="hr-001",
        title="Paid Time Off (PTO) Policy",
        source="HR Policy Portal",
        category="hr",
        summary="How PTO accrues, carryover, and booking rules for all regions.",
        content=(
            "Full-time employees accrue 20 days PTO per year (1.67 days/month). "
            "PTO must be requested at least 5 business days in advance for blocks of 3+ days. "
            "Up to 5 unused days may carry over to the next calendar year; excess is forfeited unless "
            "local law requires payout. Managers approve via Workday. "
            "Sick leave is separate: 10 days/year, no carryover. "
            "APAC and EMEA follow local statutory minimums where higher than company policy."
        ),
        tags=("pto", "leave", "vacation", "time off", "workday", "sick leave", "hr"),
    ),
    KnowledgeDoc(
        id="hr-002",
        title="Remote & Hybrid Work Policy",
        source="HR Policy Portal",
        category="hr",
        summary="Eligibility, home office stipend, and core collaboration hours.",
        content=(
            "Employees may work remotely up to 3 days per week after completing 90-day probation. "
            "Fully remote roles require VP approval and are tagged in the HR system. "
            "Core collaboration hours: 10:00–15:00 in your local timezone on in-office days. "
            "Home office stipend: $500 one-time for eligible remote/hybrid staff (receipts not required). "
            "International remote work beyond 30 days requires People Ops and Legal review."
        ),
        tags=("remote", "hybrid", "work from home", "wfh", "stipend", "hr"),
    ),
    KnowledgeDoc(
        id="hr-003",
        title="Parental & Family Leave",
        source="HR Policy Portal",
        category="hr",
        summary="Primary and secondary caregiver leave, bonding leave, and pay.",
        content=(
            "Primary caregivers: 16 weeks paid leave at 100% base salary. "
            "Secondary caregivers: 8 weeks paid at 100%. "
            "Leave must be taken within 12 months of birth, adoption, or foster placement. "
            "Notify HR at least 30 days before planned start when possible. "
            "Benefits continue during paid leave; coordinate with payroll for tax withholding changes."
        ),
        tags=("parental", "maternity", "paternity", "family leave", "adoption", "hr"),
    ),
    KnowledgeDoc(
        id="hr-004",
        title="Code of Conduct & Workplace Respect",
        source="HR Policy Portal",
        category="hr",
        summary="Expected behavior, reporting channels, and non-retaliation.",
        content=(
            "All employees must treat colleagues with respect and comply with anti-harassment policies. "
            "Conflicts of interest must be disclosed via the ethics portal within 10 days of awareness. "
            "Report concerns to your manager, HR Business Partner, or the confidential ethics hotline. "
            "Retaliation against good-faith reporters is prohibited and may result in termination."
        ),
        tags=("conduct", "ethics", "harassment", "reporting", "hr"),
    ),
    # --- Confluence / internal wiki ---
    KnowledgeDoc(
        id="conf-001",
        title="New Hire Onboarding Checklist",
        source="Confluence · People & IT",
        category="confluence",
        summary="First 30 days: accounts, training, buddy program, and equipment.",
        content=(
            "Day 1: SSO login, MFA setup, laptop pickup or shipment tracking. "
            "Week 1: Complete mandatory security and code-of-conduct training in LMS. "
            "Week 2: Meet your onboarding buddy; schedule 1:1s with manager and skip-level. "
            "Week 4: Access reviews for default tools (Slack, Jira, GitHub) — request extras via IT portal. "
            "Page owner: People Ops. Last updated: synthetic demo data."
        ),
        tags=("onboarding", "new hire", "first day", "laptop", "training", "confluence"),
    ),
    KnowledgeDoc(
        id="conf-002",
        title="Production Deployment Runbook",
        source="Confluence · Engineering",
        category="confluence",
        summary="Release windows, approvals, rollback, and on-call escalation.",
        content=(
            "Production deploys allowed Tue–Thu 14:00–18:00 UTC only, except P0 hotfixes. "
            "Requires: green CI, peer review, and change ticket (CHG-*) approved by service owner. "
            "Rollback: revert commit and run automated rollback pipeline; notify #incidents if user impact. "
            "On-call engineer is first responder; escalate to platform lead after 30 minutes unresolved."
        ),
        tags=("deploy", "production", "release", "runbook", "on-call", "engineering", "confluence"),
    ),
    KnowledgeDoc(
        id="conf-003",
        title="Internal API & Service Catalog",
        source="Confluence · Platform",
        category="confluence",
        summary="How to discover services, owners, and request API access.",
        content=(
            "All internal APIs are listed in the Service Catalog (search by domain or team). "
            "Each entry includes owner squad, SLA tier, and authentication method (OAuth, mTLS). "
            "To consume an API: open an access request in the IT portal citing catalog ID and use case. "
            "Breaking changes require 90-day deprecation notice published on #platform-announcements."
        ),
        tags=("api", "catalog", "services", "access", "platform", "confluence"),
    ),
    KnowledgeDoc(
        id="conf-004",
        title="Meeting & Documentation Standards",
        source="Confluence · Ways of Working",
        category="confluence",
        summary="When to write docs vs. meetings, templates, and decision records.",
        content=(
            "Default to async: post updates in Slack threads or Confluence before scheduling meetings. "
            "Use the ADR template for architectural decisions; link ADRs from relevant runbooks. "
            "Recurring meetings need an agenda doc and optional recorded notes within 24 hours. "
            "All project pages should list DRI, status, and last-reviewed date."
        ),
        tags=("meetings", "documentation", "adr", "confluence", "async"),
    ),
    # --- Finance policies ---
    KnowledgeDoc(
        id="fin-001",
        title="Budget Approval & Cost Center Rules",
        source="Finance Policy Hub",
        category="finance",
        summary="Who approves spend by amount and how to map cost centers.",
        content=(
            "Under $1,000: manager approval in procurement system. "
            "$1,000–$10,000: director + finance business partner. "
            "Over $10,000: VP and FP&A sign-off; capital items require CFO for >$50,000. "
            "Every purchase must tag a valid cost center; inactive centers are blocked at checkout. "
            "Quarterly true-ups: unspent budget does not roll automatically—request reallocation via FP&A."
        ),
        tags=("budget", "approval", "cost center", "procurement", "finance", "spend"),
    ),
    KnowledgeDoc(
        id="fin-002",
        title="Vendor Onboarding & Payment Terms",
        source="Finance Policy Hub",
        category="finance",
        summary="New vendor setup, W-9/W-8, and standard payment cycles.",
        content=(
            "New vendors require legal review for contracts over $5,000/year. "
            "Submit vendor form with tax documents (W-9 US, W-8 international) before first PO. "
            "Standard payment terms: Net 30 from invoice date; expedited pay requires CFO delegate approval. "
            "No personal accounts for vendor payments—use corporate procurement only."
        ),
        tags=("vendor", "invoice", "payment", "w-9", "procurement", "finance"),
    ),
    KnowledgeDoc(
        id="fin-003",
        title="Corporate Card & Spend Limits",
        source="Finance Policy Hub",
        category="finance",
        summary="Amex limits, allowed categories, and monthly reconciliation.",
        content=(
            "Corporate cards issued by role: individual limit $2,500/month default, up to $10,000 for directors. "
            "Allowed: travel, client meals, software under $500 without pre-approval. "
            "Prohibited: personal expenses, cash advances, gift cards unless pre-approved HR rewards. "
            "Reconcile all transactions in ExpenseTool within 10 business days of statement close."
        ),
        tags=("corporate card", "amex", "spend limit", "reconciliation", "finance"),
    ),
    # --- Expense policies ---
    KnowledgeDoc(
        id="exp-001",
        title="Travel & Expense (T&E) Policy",
        source="Expense Portal · Policy",
        category="expense",
        summary="Flights, hotels, per diem, and class of travel by level.",
        content=(
            "Book flights and hotels via approved corporate travel tool when possible. "
            "Economy class default; business class allowed for flights over 6 hours for Director+. "
            "Hotel cap: $250/night US tier-1 cities, $180 elsewhere unless conference block rate. "
            "Meals on travel: per diem $75/day domestic, itemized receipts required above $75 single meal. "
            "Submit expense report within 14 days of trip end; late submissions may delay reimbursement."
        ),
        tags=("travel", "expense", "flight", "hotel", "per diem", "reimbursement", "t&e"),
    ),
    KnowledgeDoc(
        id="exp-002",
        title="Receipt Requirements & Audit",
        source="Expense Portal · Policy",
        category="expense",
        summary="What receipts are required, itemization, and audit sampling.",
        content=(
            "Receipts required for all expenses $25 and above (photo or PDF in ExpenseTool). "
            "Alcohol on receipts: only with client entertainment pre-approval code. "
            "Itemize hotel folios—remove movies, minibar personal charges before submit. "
            "Finance audits 10% of reports monthly; repeated policy violations may revoke self-approval."
        ),
        tags=("receipt", "audit", "expense report", "expensetool", "reimbursement"),
    ),
    KnowledgeDoc(
        id="exp-003",
        title="Client Entertainment & Gifts",
        source="Expense Portal · Policy",
        category="expense",
        summary="Client meals, gifts, and annual caps.",
        content=(
            "Client meals: reasonable and occasional; document attendees and business purpose in ExpenseTool. "
            "Per-person meal cap $150 without VP pre-approval. "
            "Gifts to clients: max $100/person/year; no cash or cash equivalents. "
            "Gifts from clients over $50 must be disclosed to ethics portal."
        ),
        tags=("client", "entertainment", "gifts", "meals", "expense"),
    ),
    # --- Education ---
    KnowledgeDoc(
        id="edu-001",
        title="Tuition Reimbursement Program",
        source="Learning & Development Portal",
        category="education",
        summary="Eligible degrees, caps, grades, and repayment if you leave.",
        content=(
            "Up to $5,250/year for job-related degree programs (undergrad or grad). "
            "Course must be pre-approved via L&D form; degree must relate to current role or approved career path. "
            "Minimum grade B or Pass required; submit transcript within 30 days of term end. "
            "If you leave within 12 months of reimbursement, prorated amount may be clawed back."
        ),
        tags=("tuition", "reimbursement", "degree", "education", "learning", "l&d"),
    ),
    KnowledgeDoc(
        id="edu-002",
        title="Learning Stipend & Certifications",
        source="Learning & Development Portal",
        category="education",
        summary="Annual stipend for courses, books, and professional certs.",
        content=(
            "Each employee receives $1,500/year learning stipend (resets Jan 1, no carryover). "
            "Covers: online courses, technical books, conference tickets (see separate conference policy), "
            "and industry certifications (AWS, PMP, etc.). Submit receipts in L&D portal; manager approval auto for under $500. "
            "Certification exams are eligible once per cert per year."
        ),
        tags=("stipend", "certification", "courses", "learning", "education", "training"),
    ),
    KnowledgeDoc(
        id="edu-003",
        title="Conference & Event Attendance",
        source="Learning & Development Portal",
        category="education",
        summary="Approval process, travel, and share-back expectations.",
        content=(
            "Conference attendance requires manager approval and L&D budget check. "
            "Employees should submit request 6 weeks before event with business justification. "
            "After attendance: share summary in team wiki or brown-bag within 2 weeks. "
            "Max 2 paid conferences per employee per year unless VP exception."
        ),
        tags=("conference", "event", "training", "education", "learning"),
    ),
]

from bestfraiend.knowledge.extended import EXTENDED_DOCS, EXTENDED_SOURCE_LABELS

KNOWLEDGE_BASE = KNOWLEDGE_BASE + EXTENDED_DOCS

SOURCE_LABELS = {
    "hr": "HR Policy Portal",
    "confluence": "Confluence",
    "finance": "Finance Policy Hub",
    "expense": "Expense Portal",
    "education": "Learning & Development",
    **EXTENDED_SOURCE_LABELS,
}
