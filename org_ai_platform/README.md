# Org-level AI Platform

A niche web app for an **organization-level AI platform** serving **4000+ staff globally** across five departments: **HR**, **Finance**, **Operations**, **Tech**, and **Grievance**.

## What it looks like

- **Dashboard** — Hero with global context (staff count, departments), department cards (HR, Fin, Ops, Tech, Grievance), and a unified **Ask / Request** panel.
- **Ask AI** — Select department + enter a question (e.g. leave policy, expense limits).
- **Submit request** — Department, category, Employee ID, region, subject, description, priority. Categories change by department.
- **Department sections** — For each department: **top areas we serve** and **key inputs we need**.

## Top areas covered

| Department | Top areas |
|------------|-----------|
| **HR** | Leave & attendance, policies & handbook, benefits, payroll & tax, onboarding/offboarding, org structure & directory, training & learning |
| **Finance** | Expenses & reimbursements, travel & T&E, invoices & vendor payments, budgets & cost centers, approvals, audit & compliance |
| **Operations** | Facilities, travel, procurement, vendor management, assets, logistics & shipping |
| **Tech** | IT helpdesk, access requests, software & hardware, tickets, outage & status, security |
| **Grievance** | Raise a complaint, check status, anonymous reporting, policy, escalation |

## Key inputs (by department)

- **HR**: Employee ID, request type, dates, policy reference, region/country  
- **Finance**: Employee ID, cost center, amount, currency, receipt/attachment, approval level, region  
- **Operations**: Employee ID, site/region, asset type, dates, vendor name, value, justification  
- **Tech**: Employee ID, ticket type, app/system name, description, urgency, region/timezone  
- **Grievance**: Optional anonymity, category of concern, description, evidence (optional), region  

## Run the app

From the **project root** (parent of `org_ai_platform`):

```bash
.venv\Scripts\activate   # Windows
pip install fastapi uvicorn   # if not already installed

# Start and open browser
python -m org_ai_platform

# Or start only
uvicorn org_ai_platform.app:app --reload
```

Then open **http://127.0.0.1:8000**.

## API (optional)

- `POST /api/ask` — Body: `{ "department": "hr", "query": "What is leave policy?" }` → stub response.
- `POST /api/request` — Body: department, category, employee_id, region, subject, description, priority → returns a ticket ID.

Replace stubs with your AI/routing backend when integrating.
