"""Extended enterprise knowledge: onboarding, tax (NA/EU), IT, benefits."""

from bestfraiend.knowledge.data import KnowledgeDoc

EXTENDED_DOCS: list[KnowledgeDoc] = [
    # --- Onboarding ---
    KnowledgeDoc(
        id="onb-001",
        title="New Hire Day 1 Checklist",
        source="Onboarding Hub",
        category="onboarding",
        summary="Accounts, equipment, orientation, and mandatory training on your first day.",
        content=(
            "Before arrival: complete I-9 / right-to-work documentation (region-specific). "
            "Day 1: badge pickup, laptop or ship-to-home tracking, SSO and MFA enrollment. "
            "Complete Code of Conduct and Security Awareness in LMS (due within 48 hours). "
            "Meet your onboarding buddy and manager; review 30-60-90 plan in Workday. "
            "North America: enroll in benefits within 30 days of start. "
            "Europe: local HR will schedule contract signing and tax registration briefing."
        ),
        tags=("onboarding", "day 1", "new hire", "first day", "i-9", "mfa", "buddy"),
    ),
    KnowledgeDoc(
        id="onb-002",
        title="30-60-90 Day Onboarding Plan",
        source="Onboarding Hub",
        category="onboarding",
        summary="Expectations for your first three months by role family.",
        content=(
            "Days 1-30: learn systems, shadow teammates, complete role-specific training paths. "
            "Days 31-60: own small deliverables; schedule skip-level 1:1; request tool access via IT portal. "
            "Days 61-90: lead a project slice; complete probation check-in with manager and HR. "
            "Engineering: access GitHub, CI, and staging by week 2 with manager approval. "
            "All roles: probation period is 90 days unless local law requires otherwise."
        ),
        tags=("onboarding", "30-60-90", "probation", "new hire", "plan"),
    ),
    KnowledgeDoc(
        id="onb-003",
        title="Onboarding Buddy Program",
        source="Onboarding Hub",
        category="onboarding",
        summary="How buddies support new hires and what to expect.",
        content=(
            "Every new hire is paired with a buddy for the first 90 days. "
            "Buddies help with culture, tools, and navigation—not performance management. "
            "Weekly 15-min sync recommended for the first month. "
            "Questions about pay, tax, or benefits should go to HR or BestFrAIend, not only your buddy."
        ),
        tags=("onboarding", "buddy", "mentor", "new hire"),
    ),
    KnowledgeDoc(
        id="onb-004",
        title="Equipment & Workspace Setup",
        source="Onboarding Hub · IT",
        category="onboarding",
        summary="Laptop, monitors, home office, and office desk assignment.",
        content=(
            "Standard kit: laptop, charger, headset. Monitors: 1 for hybrid, 2 for full-time office upon request. "
            "Home office: stipend per Remote Work policy (see HR). "
            "Desk assignment: Facilities ticket within first week for hybrid staff. "
            "Return all equipment on offboarding—see IT asset policy."
        ),
        tags=("onboarding", "laptop", "equipment", "desk", "workspace"),
    ),
    # --- Tax North America ---
    KnowledgeDoc(
        id="tax-001",
        title="US Federal Tax Withholding (W-4)",
        source="Payroll · North America",
        category="tax",
        summary="How to complete W-4 and update withholding in Workday.",
        content=(
            "US employees complete Form W-4 in Workday Payroll within 5 days of start. "
            "Updates allowed anytime; changes apply to the next pay period. "
            "Multiple jobs or spouse income: use IRS estimator or Workday guided flow. "
            "Company does not provide personal tax advice—consult a tax professional for complex situations. "
            "Year-end W-2 available in Workday by January 31."
        ),
        tags=("tax", "w-4", "withholding", "us", "usa", "federal", "payroll", "north america"),
    ),
    KnowledgeDoc(
        id="tax-002",
        title="US State & Local Tax",
        source="Payroll · North America",
        category="tax",
        summary="State withholding, reciprocity, and remote work tax implications.",
        content=(
            "State tax withheld based on work location and residence rules in Workday. "
            "Remote workers must keep work location current—notify HR within 10 days of a move. "
            "Some states have reciprocity agreements; Workday applies defaults from your profile. "
            "Stock (RSU) income taxed as supplemental wages; see Equity Tax FAQ. "
            "Local city taxes (e.g. NYC, Philadelphia) may apply automatically."
        ),
        tags=("tax", "state", "local", "remote", "us", "withholding", "rsu", "equity"),
    ),
    KnowledgeDoc(
        id="tax-003",
        title="Canada Payroll & T4",
        source="Payroll · North America",
        category="tax",
        summary="TD1 forms, CPP/EI, and T4 slips for Canadian employees.",
        content=(
            "Complete federal and provincial TD1 in Workday at start. "
            "CPP and EI deducted per CRA rules; Quebec employees have separate provincial forms. "
            "T4 slips posted by end of February. "
            "Benefits taxable portions appear on T4—see benefits summary in portal."
        ),
        tags=("tax", "canada", "t4", "td1", "cpp", "ei", "north america", "payroll"),
    ),
    KnowledgeDoc(
        id="tax-004",
        title="RSU & Equity Tax (North America)",
        source="Payroll · Equity",
        category="tax",
        summary="How restricted stock units are taxed at vest and sale.",
        content=(
            "RSUs taxed as income at vest; company withholds shares or cash for taxes. "
            "US: supplemental withholding rate may apply on vest. "
            "Canada: included in employment income; T4 updated accordingly. "
            "Sale of shares: capital gains/loss rules apply—keep cost basis records from E*Trade / Shareworks. "
            "See Confluence 'Equity 101' for blackout windows and 10b5-1 plans."
        ),
        tags=("tax", "rsu", "equity", "stock", "vest", "us", "canada", "north america"),
    ),
    # --- Tax Europe ---
    KnowledgeDoc(
        id="tax-005",
        title="UK PAYE & Tax Code",
        source="Payroll · Europe",
        category="tax",
        summary="P45/P60, tax codes, and HMRC reporting for UK employees.",
        content=(
            "Provide P45 from prior employer or complete starter checklist in Workday. "
            "Tax code updates via HMRC notice—payroll applies automatically when received. "
            "P60 available each May for prior tax year. "
            "Student loan Plan 1/2/4 deductions configured from HMRC data. "
            "Benefits in kind (P11D): company car, private medical—reported annually."
        ),
        tags=("tax", "uk", "paye", "p45", "p60", "hmrc", "europe", "britain"),
    ),
    KnowledgeDoc(
        id="tax-006",
        title="Germany Lohnsteuer & Social Contributions",
        source="Payroll · Europe",
        category="tax",
        summary="Tax class, church tax, and social insurance for Germany.",
        content=(
            "Tax class (Steuerklasse) set at hire—change via Finanzamt notification to HR. "
            "Social contributions: health, pension, unemployment, care insurance split employer/employee. "
            "Lohnsteuerbescheinigung (annual tax certificate) by end of February. "
            "Works council and Betriebsvereinbarung may affect local benefits—see country addendum."
        ),
        tags=("tax", "germany", "lohnsteuer", "steuerklasse", "europe", "social"),
    ),
    KnowledgeDoc(
        id="tax-007",
        title="EU Cross-Border & Remote Work Tax",
        source="Payroll · Global Mobility",
        category="tax",
        summary="Working from another EU country temporarily or permanently.",
        content=(
            "Cross-border work over 30 days requires Global Mobility review before travel. "
            "Permanent moves: update work country in Workday; payroll and tax switch on effective date. "
            "A1 certificates for temporary EU assignments—request via mobility portal 4 weeks ahead. "
            "Double taxation treaties may apply; company provides generic guidance only, not personal tax advice. "
            "Brexit: UK treated as third country for EU assignments—separate checklist."
        ),
        tags=("tax", "eu", "europe", "cross-border", "remote", "mobility", "a1"),
    ),
    KnowledgeDoc(
        id="tax-008",
        title="Year-End Tax Documents (All Regions)",
        source="Payroll · Global",
        category="tax",
        summary="When W-2, T4, P60, and other forms are available.",
        content=(
            "US W-2: by Jan 31. Canada T4: by end of Feb. UK P60: by May 31 after tax year. "
            "Germany Lohnsteuerbescheinigung: by end of Feb. "
            "All documents in Workday > Pay > Tax Documents. "
            "Discrepancies: open HR ticket within 30 days of publication."
        ),
        tags=("tax", "w-2", "t4", "p60", "year-end", "documents", "global"),
    ),
    # --- IT / Security (employee essentials) ---
    KnowledgeDoc(
        id="it-001",
        title="Password, MFA & SSO",
        source="IT Service Portal",
        category="it",
        summary="Single sign-on, authenticator setup, and password reset.",
        content=(
            "Use company SSO for all approved apps. MFA required on every login. "
            "Password reset: self-service at id.company.com or IT chatbot. "
            "Lost device: report immediately to security@company.com for session revoke. "
            "Never share MFA codes or approve push notifications you did not initiate."
        ),
        tags=("it", "mfa", "sso", "password", "security", "login"),
    ),
    KnowledgeDoc(
        id="it-002",
        title="Acceptable Use & Data Handling",
        source="IT · Security Policy",
        category="it",
        summary="Customer data, PII, and approved tools for work.",
        content=(
            "Customer and employee PII only in approved systems—no personal email or unapproved cloud storage. "
            "GitHub Enterprise for code; Google Drive for docs unless team uses Confluence. "
            "Phishing: report via 'Report Phish' button in Outlook/Gmail. "
            "Annual security training mandatory; overdue training may restrict VPN access."
        ),
        tags=("it", "security", "pii", "data", "phishing", "compliance"),
    ),
    # --- Benefits (cross-region) ---
    KnowledgeDoc(
        id="ben-001",
        title="Health Benefits Enrollment (North America)",
        source="Benefits Portal",
        category="benefits",
        summary="Medical, dental, vision, HSA/FSA for US and Canada.",
        content=(
            "US: open enrollment Nov 1–15; changes effective Jan 1. New hires: 30-day window from start. "
            "Plans: PPO, HDHP with HSA option; dental and vision bundled or separate by state. "
            "Canada: provincial coverage plus employer supplemental—see province-specific guide. "
            "Life event changes (marriage, birth): 30 days to update in Workday."
        ),
        tags=("benefits", "health", "medical", "dental", "hsa", "fsa", "us", "canada", "enrollment"),
    ),
    KnowledgeDoc(
        id="ben-002",
        title="Retirement & Pension (401k / RRSP / UK Pension)",
        source="Benefits Portal",
        category="benefits",
        summary="Retirement plans by region and company match.",
        content=(
            "US 401(k): eligible after 30 days; company match 100% up to 4% of base; vesting 3-year cliff. "
            "Canada RRSP: group plan via provider; match up to 3% after 90 days. "
            "UK: auto-enrolment pension; minimum contributions per UK law; opt-out window 1 month. "
            "Change contribution % in benefits portal anytime; payroll applies next cycle."
        ),
        tags=("benefits", "401k", "rrsp", "pension", "retirement", "match", "us", "uk", "canada"),
    ),
]

EXTENDED_SOURCE_LABELS = {
    "onboarding": "Onboarding Hub",
    "tax": "Tax & Payroll",
    "it": "IT & Security",
    "benefits": "Benefits Portal",
}
