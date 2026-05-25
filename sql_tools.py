# sql_tools.py
import pyodbc
from typing import List, Dict, Any
from config import SQL_DW_CONN_STR


def get_connection():
    return pyodbc.connect(SQL_DW_CONN_STR)


def run_explain(query: str) -> Dict[str, Any]:
    """
    Run EXPLAIN for a SQL DW / Synapse query.
    Adjust if your environment uses a different syntax (e.g. SET SHOWPLAN_XML ON).
    """
    with get_connection() as cn:
        cur = cn.cursor()
        # Many Synapse DW setups support EXPLAIN <query>
        cur.execute(f"EXPLAIN {query}")
        rows = cur.fetchall()

    # Simplest: join all returned text lines
    plan_text = "\n".join(str(r[0]) for r in rows)
    return {"plan_text": plan_text}


def get_table_rowcounts() -> List[Dict[str, Any]]:
    """
    Get approximate row counts for all user tables.
    """
    sql = """
    SELECT
        s.name AS schema_name,
        t.name AS table_name,
        SUM(p.rows) AS row_count
    FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    JOIN sys.partitions p ON t.object_id = p.object_id
    WHERE p.index_id IN (0, 1)
    GROUP BY s.name, t.name
    ORDER BY row_count DESC;
    """
    with get_connection() as cn:
        cur = cn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

    return [
        {
            "schema": r[0],
            "table": r[1],
            "row_count": int(r[2]),
        }
        for r in rows
    ]


def get_index_info() -> List[Dict[str, Any]]:
    """
    Get index metadata (type, key columns).
    """
    sql = """
    SELECT
        s.name AS schema_name,
        t.name AS table_name,
        i.name AS index_name,
        i.type_desc,
        STUFF((
            SELECT ', ' + c.name
            FROM sys.index_columns ic
            JOIN sys.columns c
              ON ic.object_id = c.object_id
             AND ic.column_id = c.column_id
            WHERE ic.object_id = i.object_id
              AND ic.index_id = i.index_id
              AND ic.is_included_column = 0
            ORDER BY ic.key_ordinal
            FOR XML PATH(''), TYPE).value('.', 'nvarchar(max)'), 1, 2, ''
        ) AS key_columns
    FROM sys.indexes i
    JOIN sys.tables t ON i.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE i.is_hypothetical = 0
      AND i.index_id > 0
      AND t.is_ms_shipped = 0;
    """
    with get_connection() as cn:
        cur = cn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

    return [
        {
            "schema": r[0],
            "table": r[1],
            "index_name": r[2],
            "index_type": r[3],
            "key_columns": r[4],
        }
        for r in rows
    ]
