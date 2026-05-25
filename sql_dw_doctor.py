# sql_dw_doctor.py
from openai import OpenAI
import json
from typing import Optional
from config import OPENAI_API_KEY, OPENAI_MODEL
from sql_tools import run_explain, get_table_rowcounts, get_index_info

# Simple CLI colours
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"


client = OpenAI(api_key=OPENAI_API_KEY)


# ---- Tool schema exposed to the model ----
TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "run_explain",
            "description": "Run EXPLAIN on a SQL DW / Synapse query to get the execution plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_table_rowcounts",
            "description": "Get approximate row counts for all user tables in the data warehouse.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_index_info",
            "description": "List indexes on tables (keys and index types).",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


SYSTEM_PROMPT = """
You are an expert Azure SQL Data Warehouse / Synapse performance and cost optimization engineer.

Goals (in priority order):
1) Faster query performance
2) Scalability as data volume grows
3) Cost savings (less data scanned, fewer shuffles, less compute)

You work with analytic / warehouse workloads (star/snowflake schemas, fact/dimension tables).

For each query you analyze:
- Use tools (EXPLAIN, table stats, index info) to understand:
  - Which tables are scanned the most
  - Join patterns
  - Whether indexes and partitions are used effectively
- Assume tables may grow 10x in the next 12–24 months.

Your response must include:

1) Overview
   - Summarize what the query does and current performance risk: LOW, MEDIUM, or HIGH.

2) Bottlenecks
   - Specific issues: full table scans, skew, shuffles, spills, missing indexes, poor filtering, etc.

3) Optimization Techniques
   - Indexing:
     - Propose concrete index definitions (CREATE INDEX statements) with rationale.
   - Partitioning:
     - Suggest partition keys and granularity (e.g. monthly partitions on a date column).
   - Distribution / sharding (conceptually; do not guess exact Synapse syntax):
     - Recommend better distribution keys or replicated dimensions when appropriate.
   - Query rewrites:
     - Provide improved versions of the query or key fragments that push filters earlier,
       reduce SELECT *, and minimize intermediate rows.

4) Scaling & Cost Guidance
   - Explain how your recommendations will behave as data grows.
   - Call out trade-offs (e.g. more storage vs better performance).

5) summary_json
   - At the end, output a JSON object labeled 'summary_json' with:
     - original_query: string
     - optimized_query: string or null
     - risk_level: "LOW" | "MEDIUM" | "HIGH"
     - key_issues: list of strings
     - proposed_indexes: list of strings (CREATE INDEX ...)
     - partitioning_recommendations: list of strings
     - distribution_recommendations: list of strings
     - query_rewrite_notes: list of strings
     - cost_impact_notes: list of strings

If some information is not available (e.g. no plan details), you must say so and base your answer on what you know.
Be explicit and practical; aim to save human engineers time by being very concrete.
"""


def run_sql_dw_doctor(sql: str, runtime_ms: Optional[float] = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "You are acting as a 'SQL DW Doctor' for Azure Synapse.\n"
                f"Here is a query to tune. Approximate runtime_ms: {runtime_ms}.\n\n"
                f"QUERY:\n{sql}"
            ),
        },
    ]

    while True:
        print(f"{CYAN}🔁 Calling OpenAI with current messages...{RESET}")
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOL_SCHEMA,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        # If model wants to call tools
        if msg.tool_calls:
            print(f"{YELLOW}🧰 Model requested tools...{RESET}")
            messages.append(msg)

            for call in msg.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                print(f"{YELLOW}⚙️ Using tool: {name} with args: {args}{RESET}")

                # Dispatch to the right Python function
                if name == "run_explain":
                    result = run_explain(**args)
                elif name == "get_table_rowcounts":
                    result = get_table_rowcounts()
                elif name == "get_index_info":
                    result = get_index_info()
                else:
                    result = {"error": f"Unknown tool: {name}"}

                print(f"{CYAN}   ↳ Tool result (truncated): {str(result)[:300]}...{RESET}")

                # Add tool result back to conversation
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": name,
                        "content": json.dumps(result),
                    }
                )

            # Loop again so the model can use the tool results
            continue

        # Final answer (no more tool calls)
        print(f"{GREEN}✅ Model returned final analysis.{RESET}")
        return msg.content


def main():
    print(f"{GREEN}=== SQL DW Doctor ==={RESET}")
    print("Paste your SQL DW / Synapse query below. Finish with an empty line.\n")

    # Read multiline query from stdin
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    sql = "\n".join(lines)

    if not sql.strip():
        print(f"{RED}No query provided. Exiting.{RESET}")
        return

    runtime_str = input(
        "Optional: approximate runtime in milliseconds (or press Enter to skip): "
    ).strip()

    runtime_ms = None
    if runtime_str:
        try:
            runtime_ms = float(runtime_str)
        except ValueError:
            print(f"{YELLOW}Could not parse runtime_ms; ignoring.{RESET}")

    print(f"{CYAN}\n🔍 Analyzing query... this may take a few seconds.{RESET}\n")
    report = run_sql_dw_doctor(sql, runtime_ms=runtime_ms)

    print(f"\n{RED}=== SQL DW DOCTOR REPORT ==={RESET}\n")
    print(report)
    print(f"\n{GREEN}=== END OF REPORT ==={RESET}")


if __name__ == "__main__":
    main()
