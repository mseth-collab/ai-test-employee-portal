"""
from __future__ import annotations

# Hardcoded FAQs for BestFrAIend POC.
Categories: vacation, hr, confluence, travel, contacts.
Matched before full-text search so answers are instant and deterministic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FAQ:
    id: str
    category: str          # vacation | hr | confluence | travel | contacts
    category_label: str
    question: str          # canonical display question
    answer: str            # full answer shown in chat
    triggers: tuple[str, ...]  # keywords/phrases that trigger this FAQ


FAQS: list[FAQ] = [

    # ─── VACATION ──────────────────────────────────────────────────────────────
    FAQ(
        id="faq-vac-001",
        category="vacation",
        category_label="Vacation & PTO",
        question="How many vacation days do I get per year?",
        answer=(
            "**Vacation / PTO allowance**\n\n"
            "Full-time employees accrue **20 days PTO per year** (1.67 days/month).\n"
            "• Sick leave is separate: **10 days/year**, no carryover.\n"
            "• APAC and EMEA employees follow local statutory minimums where higher.\n"
            "• Part-time: prorated based on hours.\n\n"
            "Request time off in **Workday > Time Off**.\n"
            "_Ref: hr-001 · HR Policy Portal_"
        ),
        triggers=("how many vacation", "pto days", "vacation days", "annual leave days", "how much pto", "days off per year"),
    ),
    FAQ(
        id="faq-vac-002",
        category="vacation",
        category_label="Vacation & PTO",
        question="Can I carry over unused PTO to next year?",
        answer=(
            "**PTO carryover**\n\n"
            "Up to **5 unused PTO days** may carry over to the next calendar year.\n"
            "Excess days are forfeited unless local law requires payout (check with your regional HR).\n"
            "Sick leave does **not** carry over.\n\n"
            "Questions? → **#hr-help** on Slack or hr@company.com.\n"
            "_Ref: hr-001 · HR Policy Portal_"
        ),
        triggers=("carry over", "carryover", "rollover pto", "unused vacation", "unused pto", "pto expire", "pto rollover"),
    ),
    FAQ(
        id="faq-vac-003",
        category="vacation",
        category_label="Vacation & PTO",
        question="How do I request time off?",
        answer=(
            "**Requesting time off**\n\n"
            "1. Open **Workday** → Time Off → Request.\n"
            "2. Select dates and type (PTO, sick, bereavement, etc.).\n"
            "3. For blocks of **3 or more days**, submit at least **5 business days** in advance.\n"
            "4. Your manager approves in Workday — you'll get an email confirmation.\n\n"
            "For urgent same-day sick leave, notify your manager directly, then log in Workday.\n"
            "_Ref: hr-001 · HR Policy Portal_"
        ),
        triggers=("how to request", "request time off", "book leave", "apply leave", "apply for pto", "how do i take vacation", "book vacation"),
    ),
    FAQ(
        id="faq-vac-004",
        category="vacation",
        category_label="Vacation & PTO",
        question="What is the parental / maternity / paternity leave policy?",
        answer=(
            "**Parental leave**\n\n"
            "• **Primary caregiver**: 16 weeks paid at 100% base salary.\n"
            "• **Secondary caregiver**: 8 weeks paid at 100%.\n"
            "• Must be taken within 12 months of birth, adoption, or foster placement.\n"
            "• Notify HR at least 30 days before planned start.\n"
            "• Benefits continue during paid leave.\n\n"
            "Contact **hr@company.com** or your HR Business Partner to start the process.\n"
            "_Ref: hr-003 · HR Policy Portal_"
        ),
        triggers=("parental leave", "maternity", "paternity", "baby", "adoption leave", "family leave", "birth"),
    ),
    FAQ(
        id="faq-vac-005",
        category="vacation",
        category_label="Vacation & PTO",
        question="What is the sick leave policy?",
        answer=(
            "**Sick leave**\n\n"
            "• **10 days/year**, separate from PTO. Does not carry over.\n"
            "• No doctor's note required for 1–2 days; note required for 3+ consecutive sick days.\n"
            "• Log in Workday under **Time Off > Sick**.\n"
            "• Mental health days count as sick leave.\n\n"
            "EMEA / APAC may have higher statutory entitlements — your local policy takes precedence.\n"
            "_Ref: hr-001 · HR Policy Portal_"
        ),
        triggers=("sick leave", "sick day", "sick policy", "illness leave", "mental health day"),
    ),

    # ─── HR ─────────────────────────────────────────────────────────────────────
    FAQ(
        id="faq-hr-001",
        category="hr",
        category_label="HR",
        question="What is the remote / hybrid work policy?",
        answer=(
            "**Remote & Hybrid Work**\n\n"
            "• Employees may work remotely **up to 3 days/week** after 90-day probation.\n"
            "• Fully remote roles require **VP approval** and are tagged in the HR system.\n"
            "• **Core collaboration hours**: 10:00–15:00 in your local timezone on in-office days.\n"
            "• Home office stipend: **$500 one-time** for eligible remote/hybrid staff.\n"
            "• International remote work beyond 30 days requires People Ops + Legal review.\n\n"
            "Update your work location in **Workday** within 10 days of any move.\n"
            "_Ref: hr-002 · HR Policy Portal_"
        ),
        triggers=("remote work", "work from home", "wfh", "hybrid policy", "home office", "work remotely", "remote policy"),
    ),
    FAQ(
        id="faq-hr-002",
        category="hr",
        category_label="HR",
        question="How do I report a concern or ethics issue?",
        answer=(
            "**Reporting a concern**\n\n"
            "You have three confidential channels:\n"
            "1. **Your manager** — for day-to-day workplace issues.\n"
            "2. **HR Business Partner** — search the org directory for your HRBP.\n"
            "3. **Ethics Hotline** (anonymous) — ethics.company.com or 1-800-ETH-1234.\n\n"
            "Retaliation against good-faith reporters is **prohibited** and may result in termination.\n"
            "Conflicts of interest must be disclosed via the **ethics portal within 10 days**.\n"
            "_Ref: hr-004 · HR Policy Portal_"
        ),
        triggers=("ethics", "report concern", "harassment", "complaint", "grievance", "report issue", "report problem", "misconduct", "discrimination"),
    ),
    FAQ(
        id="faq-hr-003",
        category="hr",
        category_label="HR",
        question="When does benefits open enrollment happen?",
        answer=(
            "**Benefits open enrollment**\n\n"
            "• **US**: open enrollment **Nov 1–15**; changes effective Jan 1.\n"
            "• **New hires** (US): 30-day window from your start date.\n"
            "• **Life events** (marriage, birth, etc.): 30 days to update in Workday.\n"
            "• Canada, UK, Germany: see regional benefits guide in the Benefits Portal.\n\n"
            "Make changes in **Workday > Benefits**.\n"
            "For questions: benefits@company.com.\n"
            "_Ref: ben-001 · Benefits Portal_"
        ),
        triggers=("open enrollment", "benefits enrollment", "benefits period", "when can i change benefits", "enroll benefits"),
    ),
    FAQ(
        id="faq-hr-004",
        category="hr",
        category_label="HR",
        question="What is the performance review cycle?",
        answer=(
            "**Performance reviews**\n\n"
            "• **Mid-year check-in**: June — self-assessment + manager conversation.\n"
            "• **Annual review**: November — formal ratings, promotion decisions, comp adjustments.\n"
            "• **New hires**: 90-day probation review with manager.\n"
            "• Calibration happens in December; comp changes effective Jan 1.\n\n"
            "Access your review form in **Workday > Performance**.\n"
            "For more: #hr-help on Slack.\n"
            "_Source: HR Policy Portal_"
        ),
        triggers=("performance review", "annual review", "mid-year review", "review cycle", "promotion cycle", "calibration"),
    ),
    FAQ(
        id="faq-hr-005",
        category="hr",
        category_label="HR",
        question="How do I update my personal information (address, bank, tax)?",
        answer=(
            "**Updating personal info**\n\n"
            "• **Home address**: Workday > Personal > Contact Information. Update within 10 days of a move (tax implications).\n"
            "• **Bank / direct deposit**: Workday > Pay > Payment Elections.\n"
            "• **Tax withholding (W-4 / TD1)**: Workday > Pay > Withholding.\n"
            "• **Emergency contact**: Workday > Personal > Emergency Contacts.\n\n"
            "Changes to address may require payroll to recalculate state/provincial tax—allow 1–2 pay cycles.\n"
            "_Source: HR Policy Portal · Payroll_"
        ),
        triggers=("update address", "change address", "update bank", "direct deposit", "change withholding", "update personal info", "emergency contact"),
    ),

    # ─── CONFLUENCE / INTERNAL WIKI ─────────────────────────────────────────────
    FAQ(
        id="faq-conf-001",
        category="confluence",
        category_label="Confluence / Internal Wiki",
        question="Where do I find runbooks and technical documentation?",
        answer=(
            "**Runbooks & technical docs**\n\n"
            "• **Confluence > Engineering > Runbooks** — production deploys, incident response, rollback.\n"
            "• **Service Catalog** (Confluence > Platform) — all internal APIs with owner, SLA, auth method.\n"
            "• **ADR log** (Confluence > Architecture) — architectural decision records.\n\n"
            "Quick tips:\n"
            "• Use Confluence search with label `runbook` to filter.\n"
            "• Each service's `README` links to its primary runbook.\n"
            "• On-call engineer is listed in **PagerDuty** for live incidents.\n"
            "_Ref: conf-001, conf-002 · Confluence · Engineering_"
        ),
        triggers=("runbook", "runbooks", "technical doc", "where are docs", "engineering docs", "incident doc", "confluence engineering"),
    ),
    FAQ(
        id="faq-conf-002",
        category="confluence",
        category_label="Confluence / Internal Wiki",
        question="How do I get access to Confluence?",
        answer=(
            "**Confluence access**\n\n"
            "• All employees get read access to public spaces via SSO on day 1.\n"
            "• To **edit or create** pages: open an access request in the **IT Portal** and select *Confluence Editor*.\n"
            "• Space-level access (e.g. Engineering, Security): request via the space admin — listed in each space's sidebar.\n"
            "• Guest / contractor access: raised via your manager in the IT Portal.\n\n"
            "Login: confluence.company.com → Use company SSO.\n"
            "_Ref: conf-001 · IT Service Portal_"
        ),
        triggers=("confluence access", "access confluence", "access to confluence", "get access to confluence", "can't access confluence", "confluence login", "confluence permission"),
    ),
    FAQ(
        id="faq-conf-003",
        category="confluence",
        category_label="Confluence / Internal Wiki",
        question="What are the documentation standards for new projects?",
        answer=(
            "**Documentation standards**\n\n"
            "• Every project needs a Confluence page with: **DRI**, **status**, **last-reviewed date**.\n"
            "• Use the **ADR template** for architectural decisions; link ADRs from runbooks.\n"
            "• Prefer **async written updates** (Confluence/Slack) over recurring meetings.\n"
            "• Recurring meetings require a linked agenda doc and notes within **24 hours**.\n"
            "• Breaking API changes: 90-day deprecation notice in **#platform-announcements**.\n\n"
            "_Ref: conf-003, conf-004 · Confluence · Ways of Working_"
        ),
        triggers=("documentation standard", "doc standard", "how to document", "confluence template", "project page", "adr template"),
    ),
    FAQ(
        id="faq-conf-004",
        category="confluence",
        category_label="Confluence / Internal Wiki",
        question="What are the production deployment rules?",
        answer=(
            "**Production deployment rules**\n\n"
            "• **Deploy window**: Tue–Thu, **14:00–18:00 UTC** only (except P0 hotfixes).\n"
            "• Requirements: green CI, peer-reviewed PR, approved change ticket (**CHG-**).\n"
            "• **Rollback**: revert commit + automated rollback pipeline. Notify **#incidents** if user impact.\n"
            "• On-call engineer is first responder; escalate to platform lead after **30 min** unresolved.\n\n"
            "Full runbook: Confluence > Engineering > Production Deployment Runbook.\n"
            "_Ref: conf-002 · Confluence · Engineering_"
        ),
        triggers=("deploy", "deployment", "production deploy", "release window", "deploy rules", "how to deploy", "rollback"),
    ),

    # ─── TRAVEL ─────────────────────────────────────────────────────────────────
    FAQ(
        id="faq-trv-001",
        category="travel",
        category_label="Travel & Expenses",
        question="What is the hotel rate limit when traveling for work?",
        answer=(
            "**Hotel limits**\n\n"
            "• US Tier-1 cities (NYC, SF, LA, Chicago): **$250/night**.\n"
            "• All other US cities: **$180/night**.\n"
            "• Europe: €200/night in major cities; €150 elsewhere.\n"
            "• Conference block rates are exempt — book through the event portal.\n\n"
            "Book via the **corporate travel tool** (Concur) when possible.\n"
            "Exceptions (e.g. sold-out events): email travel@company.com with justification.\n"
            "_Ref: exp-001 · Expense Portal_"
        ),
        triggers=("hotel limit", "hotel cap", "hotel rate", "how much hotel", "hotel cost", "accommodation limit"),
    ),
    FAQ(
        id="faq-trv-002",
        category="travel",
        category_label="Travel & Expenses",
        question="What class can I fly for work travel?",
        answer=(
            "**Flight class policy**\n\n"
            "• **Default**: Economy class for all employees.\n"
            "• **Business class**: allowed for flights **over 6 hours** for Director-level and above.\n"
            "• Premium Economy upgrade: allowable for all levels on 6+ hour flights if price difference < $200 vs. economy.\n"
            "• Book through **Concur** or the approved travel agent. Out-of-policy bookings require VP pre-approval.\n\n"
            "_Ref: exp-001 · Expense Portal · T&E Policy_"
        ),
        triggers=("flight class", "business class", "economy class", "class of travel", "fly business", "upgrade flight", "can i fly", "what class", "flight policy"),
    ),
    FAQ(
        id="faq-trv-003",
        category="travel",
        category_label="Travel & Expenses",
        question="What is the daily meal / per diem allowance?",
        answer=(
            "**Meal & per diem**\n\n"
            "• Domestic (US): **$75/day** per diem — no receipts needed if under this.\n"
            "• Single meal over $75: itemized receipt required.\n"
            "• Client meals: document attendees and business purpose; per-person cap **$150** without VP pre-approval.\n"
            "• Alcohol: only with a pre-approval client entertainment code.\n"
            "• International rates vary — see the T&E per diem table in Confluence.\n\n"
            "_Ref: exp-001, exp-003 · Expense Portal_"
        ),
        triggers=("per diem", "meal allowance", "daily allowance", "food allowance", "meal limit", "how much meals", "meal expense"),
    ),
    FAQ(
        id="faq-trv-004",
        category="travel",
        category_label="Travel & Expenses",
        question="How do I submit an expense report?",
        answer=(
            "**Submitting expenses**\n\n"
            "1. Open **ExpenseTool** (expensetool.company.com).\n"
            "2. Create a new report; attach receipts (photo or PDF) for any item **$25 or above**.\n"
            "3. Tag each line with a **cost center** and trip purpose.\n"
            "4. Submit within **14 days of trip end**.\n"
            "5. Manager approves; reimbursement hits your account in the next payroll cycle.\n\n"
            "Late submissions (>30 days) require Finance Director approval.\n"
            "_Ref: exp-001, exp-002 · Expense Portal_"
        ),
        triggers=("submit expense", "expense report", "how to submit", "file expense", "expense claim", "reimbursement"),
    ),
    FAQ(
        id="faq-trv-005",
        category="travel",
        category_label="Travel & Expenses",
        question="What receipts do I need to keep?",
        answer=(
            "**Receipt requirements**\n\n"
            "• Required for **all expenses $25 and above** — photo or PDF in ExpenseTool.\n"
            "• Hotel folios: itemize; remove personal charges (movies, minibar) before submitting.\n"
            "• Alcohol on receipts: only with client entertainment pre-approval code.\n"
            "• Finance audits ~10% of reports monthly — repeated violations may revoke self-approval rights.\n\n"
            "_Ref: exp-002 · Expense Portal_"
        ),
        triggers=("receipt", "keep receipt", "need receipt", "receipt required", "receipt rules", "what receipts"),
    ),
    FAQ(
        id="faq-trv-006",
        category="travel",
        category_label="Travel & Expenses",
        question="Can I book personal travel with my corporate card?",
        answer=(
            "**Corporate card — personal use**\n\n"
            "**No.** The corporate card is for business expenses only.\n"
            "• Prohibited: personal expenses, cash advances, gift cards (unless pre-approved HR rewards).\n"
            "• Monthly default limit: **$2,500** for individual contributors; up to **$10,000** for directors.\n"
            "• Reconcile all charges in ExpenseTool within **10 business days** of statement close.\n\n"
            "Misuse may result in card suspension and disciplinary action.\n"
            "_Ref: fin-003 · Finance Policy Hub_"
        ),
        triggers=("corporate card personal", "personal on corp card", "use corporate card", "card limit", "amex personal", "corporate card rules"),
    ),

    # ─── POINTS OF CONTACT ───────────────────────────────────────────────────────
    FAQ(
        id="faq-poc-001",
        category="contacts",
        category_label="Points of Contact",
        question="Who do I contact for HR issues?",
        answer=(
            "**HR contacts**\n\n"
            "| Need | Contact |\n"
            "|------|---------|\n"
            "| General HR / policies | hr@company.com |\n"
            "| Your HR Business Partner | Org directory > HRBP column |\n"
            "| Payroll (pay slips, tax forms) | payroll@company.com |\n"
            "| Benefits (enrollment, claims) | benefits@company.com |\n"
            "| Ethics / anonymous concern | ethics.company.com · 1-800-ETH-1234 |\n"
            "| Leave / Workday issues | Workday helpdesk in the IT Portal |\n\n"
            "Slack: **#hr-help** for non-sensitive questions (team responds within 1 business day)."
        ),
        triggers=("hr contact", "contact hr", "contact for hr", "who do i contact for hr", "who do i ask hr", "hr email", "hr slack", "hr team", "hr help", "people ops contact"),
    ),
    FAQ(
        id="faq-poc-002",
        category="contacts",
        category_label="Points of Contact",
        question="Who do I contact for IT / tech support?",
        answer=(
            "**IT & Tech support contacts**\n\n"
            "| Need | Contact |\n"
            "|------|---------|\n"
            "| Helpdesk (general) | it-help@company.com · IT Portal |\n"
            "| Password / MFA reset | id.company.com (self-service) |\n"
            "| VPN / access issues | IT Portal > Access Request |\n"
            "| Security incident / phishing | security@company.com (urgent) |\n"
            "| Software license request | IT Portal > Software |\n"
            "| Laptop / hardware | IT Portal > Hardware Request |\n\n"
            "Slack: **#it-support** (response < 4 hours during business hours)."
        ),
        triggers=("it contact", "it support", "tech support", "contact it", "it help", "who do i contact for it", "it desk", "helpdesk", "support contact"),
    ),
    FAQ(
        id="faq-poc-003",
        category="contacts",
        category_label="Points of Contact",
        question="Who do I contact for Finance / expenses?",
        answer=(
            "**Finance contacts**\n\n"
            "| Need | Contact |\n"
            "|------|---------|\n"
            "| Expense reimbursements | finance@company.com |\n"
            "| Travel booking / Concur | travel@company.com |\n"
            "| Budget / cost center | Your Finance Business Partner (FP&A) |\n"
            "| Vendor / invoice payments | ap@company.com |\n"
            "| Corporate card | corpcard@company.com |\n\n"
            "Slack: **#finance-help** · Finance office hours: Wednesdays 15:00 UTC via Zoom."
        ),
        triggers=("finance contact", "contact finance", "who handles expenses", "expense contact", "who approves", "finance team", "ap contact"),
    ),
    FAQ(
        id="faq-poc-004",
        category="contacts",
        category_label="Points of Contact",
        question="Who do I contact for Confluence / IT access?",
        answer=(
            "**Confluence & tool access contacts**\n\n"
            "| Need | Contact |\n"
            "|------|---------|\n"
            "| Confluence read/edit access | IT Portal > Access Request > Confluence |\n"
            "| Confluence space admin | Space sidebar > Space Details > Admin |\n"
            "| GitHub Enterprise access | IT Portal > Access Request > GitHub |\n"
            "| New SaaS tool request | IT Portal > Software Request |\n"
            "| Internal API access | Service Catalog (Confluence) > open access request |\n\n"
            "Slack: **#it-support** or **#platform-eng** for API-related questions."
        ),
        triggers=("confluence contact", "who manages confluence", "access request contact", "github access", "tool access", "saas access"),
    ),
    FAQ(
        id="faq-poc-005",
        category="contacts",
        category_label="Points of Contact",
        question="Who is my onboarding contact or buddy?",
        answer=(
            "**Onboarding contacts**\n\n"
            "| Need | Contact |\n"
            "|------|---------|\n"
            "| Onboarding questions (general) | onboarding@company.com |\n"
            "| Your onboarding buddy | Check your calendar invite from People Ops |\n"
            "| Equipment / laptop issues | IT Portal > Hardware |\n"
            "| Benefits enrollment | benefits@company.com |\n"
            "| Day 1 schedule | Your manager + Onboarding Hub in Confluence |\n\n"
            "New hire Slack channel: **#new-hires-[month-year]** (e.g. #new-hires-may-2026)."
        ),
        triggers=("onboarding contact", "who is my buddy", "onboarding buddy", "new hire contact", "who do i ask onboarding", "first day contact", "day 1 contact"),
    ),
]

# ── Index for fast lookup ────────────────────────────────────────────────────

CATEGORY_LABELS = {
    "vacation": "Vacation & PTO",
    "hr": "HR",
    "confluence": "Confluence / Internal Wiki",
    "travel": "Travel & Expenses",
    "contacts": "Points of Contact",
}


def match_faq(query: str) -> FAQ | None:
    """Return the best-matching FAQ for a query, or None."""
    lower = query.lower()
    best: FAQ | None = None
    best_score = 0
    for faq in FAQS:
        score = sum(1 for t in faq.triggers if t in lower)
        if score > best_score:
            best_score = score
            best = faq
    return best if best_score > 0 else None


def list_faqs_by_category() -> dict[str, list[dict]]:
    """Group FAQs by category for the API and UI."""
    result: dict[str, list[dict]] = {}
    for faq in FAQS:
        result.setdefault(faq.category, []).append({
            "id": faq.id,
            "category": faq.category,
            "category_label": faq.category_label,
            "question": faq.question,
        })
    return result
