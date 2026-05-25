# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json
import re

app = FastAPI(
    title="SQL Performance Doctor",
    description="Generic AI-based SQL / DW performance and cost optimization assistant.",
    version="0.2.0",
)

client = OpenAI(api_key=OPENAI_API_KEY)


# ---------- Request/Response Models ----------

class QueryContext(BaseModel):
    warehouse_type: Optional[str] = Field(
        default=None,
        description="e.g. 'Azure SQL DW', 'Synapse', 'Snowflake', 'Redshift', 'Postgres'.",
    )
    estimated_runtime_ms: Optional[float] = Field(
        default=None, description="Approx runtime in ms, if known."
    )
    data_volume_hint: Optional[str] = Field(
        default=None,
        description="High-level info like 'FactSales ~1B rows, DimCustomer ~10M rows'.",
    )
    can_change_schema: Optional[bool] = Field(
        default=True,
        description="If false, focus only on query rewrites (no new indexes/partitions).",
    )
    business_priority: Optional[str] = Field(
        default=None,
        description="e.g. 'cost savings', 'latency', 'concurrency', 'mixed'.",
    )


class AnalyzeRequest(BaseModel):
    sql: str = Field(..., description="The SQL query to analyze and tune.")
    context: Optional[QueryContext] = Field(
        default=None, description="Optional context about runtime, DW, and constraints."
    )


class AnalyzeResponse(BaseModel):
    report: str = Field(..., description="Human-readable report with clear sections.")
    summary_json: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Structured summary of findings and recommendations (if parsed successfully).",
    )


# ---------- System Prompt (more readable & structured) ----------

SYSTEM_PROMPT = """
You are a senior SQL data warehouse performance and cost optimization expert.

You work GENERICALLY across engines (Azure SQL DW / Synapse, Snowflake, Redshift, BigQuery, Postgres, etc.).
The user may not give you engine-specific details, so:

- Use engine-agnostic best practices.
- When engine-specific options (like distribution keys, partitions, columnstore) are relevant,
  explain them conceptually (e.g., "use a hash distribution on the main join key if supported").

Goals in priority order:
1) Faster query performance (lower latency, fewer timeouts)
2) Scalability as data volume grows (assume 10x growth)
3) Cost savings (less data scanned, fewer shuffles, less compute/slots/DWU)

Your response MUST be very clear and easy to read.
Use markdown headings and bullet points.

For each SQL query you analyze, structure your answer EXACTLY like this:

## Executive Summary
- Risk level: <LOW/MEDIUM/HIGH>
- Main issue: <one sentence>
- Top 3 actions:
  1) ...
  2) ...
  3) ...

## Overview
- Briefly describe what the query is doing (joins, filters, aggregations).

## Bottlenecks
- List the key performance and cost issues as bullet points.

## Indexing Recommendations
- Suggest concrete indexes (CREATE INDEX statements) and explain why each helps.

## Partitioning Recommendations
- Suggest partition keys and granularity (e.g., monthly on a date column) and how this helps with pruning and growth.

## Query Rewrite Suggestions
- Show specific rewritten snippets or patterns:
  - Avoid SELECT *
  - Push filters earlier
  - Aggregate earlier
  - Reduce unnecessary columns and joins

## Scaling & Cost Impact
- Explain how your recommendations help when data grows 10x.
- Call out trade-offs (e.g., more storage for indexes vs faster reads).

At the very end of your answer, output a JSON object labeled exactly 'summary_json' on its own line,
followed by a valid JSON object with fields:

summary_json
{
  "original_query": string,
  "optimized_query": string or null,
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "key_issues": [string, ...],
  "proposed_indexes": [string, ...],
  "partitioning_recommendations": [string, ...],
  "query_rewrite_notes": [string, ...],
  "cost_impact_notes": [string, ...]
}

Make sure the JSON is valid (double quotes, no trailing commas).
Be explicit and concrete. Avoid vague advice.
If you lack some info (like engine or table sizes), state assumptions clearly.
"""


# ---------- Helper: split human report and summary_json ----------

def split_report_and_summary(full_text: str) -> (str, Optional[Dict[str, Any]]):
    """
    Look for a line starting with 'summary_json' and a JSON object after it.
    Return (clean_report_text, parsed_summary_dict_or_None).
    """
    # Regex: 'summary_json' line, followed by a JSON object
    match = re.search(r"summary_json\s*\n({.*})", full_text, re.DOTALL)
    if not match:
        # No JSON found; return full text as report
        return full_text.strip(), None

    json_str = match.group(1).strip()
    report_text = full_text[: match.start()].rstrip()

    try:
        summary = json.loads(json_str)
    except json.JSONDecodeError:
        summary = None

    return report_text, summary


# ---------- Core Analysis Logic ----------

def generate_sql_doctor_report(sql: str, ctx: QueryContext | None) -> (str, Optional[Dict[str, Any]]):
    context_text_parts = []

    if ctx:
        if ctx.warehouse_type:
            context_text_parts.append(f"Warehouse type: {ctx.warehouse_type}.")
        if ctx.estimated_runtime_ms is not None:
            context_text_parts.append(
                f"Approximate runtime: {ctx.estimated_runtime_ms} ms."
            )
        if ctx.data_volume_hint:
            context_text_parts.append(f"Data volume hint: {ctx.data_volume_hint}.")
        if ctx.can_change_schema is False:
            context_text_parts.append(
                "Constraint: Schema cannot be changed; focus only on query rewrites and configuration."
            )
        if ctx.business_priority:
            context_text_parts.append(f"Business priority: {ctx.business_priority}.")

    context_text = "\n".join(context_text_parts) if context_text_parts else "No extra context provided."

    user_prompt = (
        "Analyze and tune the following SQL query for performance, scalability, and cost.\n\n"
        f"{context_text}\n\n"
        "SQL QUERY:\n"
        f"{sql}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
    )

    full_text = completion.choices[0].message.content or ""
    report_text, summary = split_report_and_summary(full_text)
    return report_text, summary


# ---------- FastAPI endpoints ----------

@app.post("/analyze-sql", response_model=AnalyzeResponse)
async def analyze_sql(req: AnalyzeRequest) -> AnalyzeResponse:
    report, summary = generate_sql_doctor_report(req.sql, req.context)
    return AnalyzeResponse(report=report, summary_json=summary)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
