"""
Database Plugin Interface and Implementations
============================================

This module provides database-agnostic plugins for query execution,
metrics collection, and performance monitoring across different database platforms.
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class DatabasePlugin(ABC):
    """Abstract base class for database-specific plugins."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish database connection."""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Close database connection."""
        pass
    
    @abstractmethod
    async def execute_query(self, sql: str) -> bool:
        """Execute a SQL query and return success status."""
        pass
    
    @abstractmethod
    async def get_execution_plan(self, sql: str) -> str:
        """Get the execution plan for a SQL query."""
        pass
    
    @abstractmethod
    async def get_query_statistics(self, sql: str) -> Dict[str, Any]:
        """Get query performance statistics."""
        pass
    
    @abstractmethod
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-level performance metrics."""
        pass
    
    @abstractmethod
    async def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get statistics for all tables."""
        pass
    
    @abstractmethod
    async def get_index_information(self) -> List[Dict[str, Any]]:
        """Get index information for all tables."""
        pass


class SQLServerPlugin(DatabasePlugin):
    """SQL Server specific implementation."""
    
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        try:
            import pyodbc
            self.pyodbc = pyodbc
        except ImportError:
            raise ImportError("pyodbc is required for SQL Server support")
    
    async def connect(self) -> bool:
        """Connect to SQL Server."""
        try:
            self.connection = self.pyodbc.connect(self.connection_string)
            return True
        except Exception as e:
            print(f"Failed to connect to SQL Server: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from SQL Server."""
        if self.connection:
            self.connection.close()
    
    async def execute_query(self, sql: str) -> bool:
        """Execute a SQL query."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            # For SELECT queries, fetch results to ensure execution completes
            try:
                cursor.fetchall()
            except:
                pass  # Non-SELECT queries don't return results
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Query execution failed: {e}")
            return False
    
    async def get_execution_plan(self, sql: str) -> str:
        """Get SQL Server execution plan."""
        try:
            cursor = self.connection.cursor()
            
            # Use SET SHOWPLAN_TEXT ON for execution plan
            cursor.execute("SET SHOWPLAN_TEXT ON")
            cursor.execute(sql)
            
            plan_lines = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                plan_lines.append(row[0])
            
            cursor.execute("SET SHOWPLAN_TEXT OFF")
            return "\n".join(plan_lines)
        except Exception as e:
            return f"Failed to get execution plan: {e}"
    
    async def get_query_statistics(self, sql: str) -> Dict[str, Any]:
        """Get SQL Server query statistics."""
        try:
            cursor = self.connection.cursor()
            
            # Enable statistics
            cursor.execute("SET STATISTICS IO ON")
            cursor.execute("SET STATISTICS TIME ON")
            cursor.execute(sql)
            
            # This would require parsing the output, which is complex
            # For now, return basic info
            return {
                "platform": "SQL Server",
                "statistics_enabled": True,
                "note": "Detailed statistics require output parsing"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get SQL Server system metrics."""
        try:
            cursor = self.connection.cursor()
            
            # Query system DMVs for performance metrics
            queries = [
                # CPU usage
                """
                SELECT 
                    SUM(qs.total_worker_time) / 1000 as total_cpu_ms,
                    SUM(qs.execution_count) as total_executions
                FROM sys.dm_exec_query_stats qs
                """,
                # Memory usage
                """
                SELECT 
                    (physical_memory_in_use_kb / 1024) as memory_used_mb,
                    (locked_page_allocations_kb / 1024) as locked_memory_mb
                FROM sys.dm_os_process_memory
                """,
                # I/O metrics
                """
                SELECT 
                    SUM(user_seeks + user_scans + user_lookups) as total_reads,
                    SUM(user_updates) as total_writes
                FROM sys.dm_db_index_usage_stats
                """
            ]
            
            metrics = {}
            for i, query in enumerate(queries):
                try:
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if row:
                        if i == 0:
                            metrics.update({
                                "total_cpu_ms": row[0],
                                "total_executions": row[1]
                            })
                        elif i == 1:
                            metrics.update({
                                "memory_used_mb": row[0],
                                "locked_memory_mb": row[1]
                            })
                        elif i == 2:
                            metrics.update({
                                "total_reads": row[0],
                                "total_writes": row[1]
                            })
                except:
                    continue
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get SQL Server table statistics."""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                s.name as schema_name,
                t.name as table_name,
                SUM(p.rows) as row_count,
                SUM(a.total_pages) * 8 as total_space_kb,
                SUM(a.used_pages) * 8 as used_space_kb
            FROM sys.tables t
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            INNER JOIN sys.partitions p ON t.object_id = p.object_id
            INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            WHERE p.index_id <= 1
            GROUP BY s.name, t.name
            ORDER BY SUM(p.rows) DESC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "row_count": row[2],
                    "total_space_kb": row[3],
                    "used_space_kb": row[4]
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_index_information(self) -> List[Dict[str, Any]]:
        """Get SQL Server index information."""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                s.name as schema_name,
                t.name as table_name,
                i.name as index_name,
                i.type_desc,
                STUFF((
                    SELECT ', ' + c.name
                    FROM sys.index_columns ic
                    JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                    WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 0
                    ORDER BY ic.key_ordinal
                    FOR XML PATH('')
                ), 1, 2, '') as key_columns
            FROM sys.indexes i
            JOIN sys.tables t ON i.object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE i.is_hypothetical = 0 AND i.index_id > 0
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "index_name": row[2],
                    "index_type": row[3],
                    "key_columns": row[4]
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]


class AzureSynapsePlugin(DatabasePlugin):
    """Azure Synapse Analytics specific implementation."""
    
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        try:
            import pyodbc
            self.pyodbc = pyodbc
        except ImportError:
            raise ImportError("pyodbc is required for Azure Synapse support")
    
    async def connect(self) -> bool:
        """Connect to Azure Synapse."""
        try:
            self.connection = self.pyodbc.connect(self.connection_string)
            return True
        except Exception as e:
            print(f"Failed to connect to Azure Synapse: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Azure Synapse."""
        if self.connection:
            self.connection.close()
    
    async def execute_query(self, sql: str) -> bool:
        """Execute a SQL query on Azure Synapse."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            # For SELECT queries, fetch results
            try:
                cursor.fetchall()
            except:
                pass
            return True
        except Exception as e:
            print(f"Query execution failed: {e}")
            return False
    
    async def get_execution_plan(self, sql: str) -> str:
        """Get Azure Synapse execution plan using EXPLAIN."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"EXPLAIN {sql}")
            
            plan_lines = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                plan_lines.append(str(row[0]))
            
            return "\n".join(plan_lines)
        except Exception as e:
            return f"Failed to get execution plan: {e}"
    
    async def get_query_statistics(self, sql: str) -> Dict[str, Any]:
        """Get Azure Synapse query statistics."""
        try:
            # Azure Synapse has specific DMVs for monitoring
            cursor = self.connection.cursor()
            
            # Get distributed query statistics
            stats_query = """
            SELECT 
                COUNT(*) as total_requests,
                AVG(DATEDIFF(millisecond, request_start_time, end_time)) as avg_duration_ms,
                SUM(DATEDIFF(millisecond, request_start_time, end_time)) as total_duration_ms
            FROM sys.dm_pdw_exec_requests
            WHERE database_name = DB_NAME()
            """
            
            cursor.execute(stats_query)
            row = cursor.fetchone()
            
            return {
                "platform": "Azure Synapse",
                "total_requests": row[0] if row else 0,
                "avg_duration_ms": row[1] if row else 0,
                "total_duration_ms": row[2] if row else 0
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get Azure Synapse system metrics."""
        try:
            cursor = self.connection.cursor()
            
            # Get warehouse-specific metrics
            queries = [
                # Data warehouse units
                """
                SELECT 
                    s.service_level,
                    s.current_dwu
                FROM sys.dm_pdw_service_sessions s
                WHERE s.session_id = @@SPID
                """,
                # Query activity
                """
                SELECT 
                    COUNT(*) as active_queries,
                    AVG(DATEDIFF(millisecond, request_start_time, end_time)) as avg_query_duration
                FROM sys.dm_pdw_exec_requests
                WHERE status = 'Running'
                """
            ]
            
            metrics = {}
            for query in queries:
                try:
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if row:
                        metrics.update({
                            "service_level": row[0] if len(row) > 0 else "Unknown",
                            "current_dwu": row[1] if len(row) > 1 else 0
                        })
                        break
                except:
                    continue
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get Azure Synapse table statistics."""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                s.name as schema_name,
                t.name as table_name,
                t.distribution_type,
                COUNT(p.partition_number) as partition_count
            FROM sys.tables t
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            INNER JOIN sys.pdw_table_distribution_properties p ON t.object_id = p.object_id
            GROUP BY s.name, t.name, t.distribution_type
            ORDER BY s.name, t.name
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "distribution_type": row[2],
                    "partition_count": row[3]
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_index_information(self) -> List[Dict[str, Any]]:
        """Get Azure Synapse index information (clustered columnstore is default)."""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                s.name as schema_name,
                t.name as table_name,
                i.name as index_name,
                i.type_desc as index_type,
                CASE 
                    WHEN i.type_desc = 'CLUSTERED COLUMNSTORE' THEN 'Columnstore - Primary'
                    WHEN i.type_desc = 'HEAP' THEN 'Heap - No indexes'
                    ELSE 'Other'
                END as index_description
            FROM sys.indexes i
            JOIN sys.tables t ON i.object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE i.index_id >= 0
            ORDER BY s.name, t.name
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "index_name": row[2],
                    "index_type": row[3],
                    "description": row[4]
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]


class PostgreSQLPlugin(DatabasePlugin):
    """PostgreSQL specific implementation."""
    
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        try:
            import asyncpg
            self.asyncpg = asyncpg
        except ImportError:
            raise ImportError("asyncpg is required for PostgreSQL support")
    
    async def connect(self) -> bool:
        """Connect to PostgreSQL."""
        try:
            self.connection = await self.asyncpg.connect(self.connection_string)
            return True
        except Exception as e:
            print(f"Failed to connect to PostgreSQL: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from PostgreSQL."""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, sql: str) -> bool:
        """Execute a SQL query on PostgreSQL."""
        try:
            await self.connection.execute(sql)
            return True
        except Exception as e:
            print(f"Query execution failed: {e}")
            return False
    
    async def get_execution_plan(self, sql: str) -> str:
        """Get PostgreSQL execution plan using EXPLAIN."""
        try:
            plan = await self.connection.fetch("EXPLAIN (ANALYZE, BUFFERS) " + sql)
            return "\n".join([str(row['QUERY PLAN']) for row in plan])
        except Exception as e:
            return f"Failed to get execution plan: {e}"
    
    async def get_query_statistics(self, sql: str) -> Dict[str, Any]:
        """Get PostgreSQL query statistics."""
        try:
            # Get database statistics
            stats_query = """
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_tuples,
                n_dead_tup as dead_tuples
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
            LIMIT 10
            """
            
            rows = await self.connection.fetch(stats_query)
            
            return {
                "platform": "PostgreSQL",
                "table_stats": [
                    {
                        "schema": row['schemaname'],
                        "table": row['tablename'],
                        "inserts": row['inserts'],
                        "updates": row['updates'],
                        "deletes": row['deletes'],
                        "live_tuples": row['live_tuples'],
                        "dead_tuples": row['dead_tuples']
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get PostgreSQL system metrics."""
        try:
            # Get database-wide statistics
            query = """
            SELECT 
                numbackends as active_connections,
                xact_commit as transactions_committed,
                xact_rollback as transactions_rolled_back,
                blks_read as blocks_read,
                blks_hit as blocks_hit,
                tup_returned as tuples_returned,
                tup_fetched as tuples_fetched
            FROM pg_stat_database
            WHERE datname = current_database()
            """
            
            row = await self.connection.fetchrow(query)
            
            if row:
                return {
                    "active_connections": row['active_connections'],
                    "transactions_committed": row['transactions_committed'],
                    "transactions_rolled_back": row['transactions_rolled_back'],
                    "blocks_read": row['blocks_read'],
                    "blocks_hit": row['blocks_hit'],
                    "cache_hit_ratio": row['blocks_hit'] / (row['blocks_hit'] + row['blocks_read']) if (row['blocks_hit'] + row['blocks_read']) > 0 else 0
                }
            else:
                return {"error": "No statistics available"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get PostgreSQL table statistics."""
        try:
            query = """
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_tuples,
                n_dead_tuples as dead_tuples,
                last_vacuum,
                last_autovacuum,
                last_analyze,
                last_autoanalyze
            FROM pg_stat_user_tables
            ORDER BY n_live_tuples DESC
            """
            
            rows = await self.connection.fetch(query)
            
            return [
                {
                    "schema": row['schemaname'],
                    "table": row['tablename'],
                    "inserts": row['inserts'],
                    "updates": row['updates'],
                    "deletes": row['deletes'],
                    "live_tuples": row['live_tuples'],
                    "dead_tuples": row['dead_tuples'],
                    "last_vacuum": str(row['last_vacuum']),
                    "last_autovacuum": str(row['last_autovacuum']),
                    "last_analyze": str(row['last_analyze']),
                    "last_autoanalyze": str(row['last_autoanalyze'])
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_index_information(self) -> List[Dict[str, Any]]:
        """Get PostgreSQL index information."""
        try:
            query = """
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
            ORDER BY schemaname, tablename, indexname
            """
            
            rows = await self.connection.fetch(query)
            
            return [
                {
                    "schema": row['schemaname'],
                    "table": row['tablename'],
                    "index_name": row['indexname'],
                    "index_definition": row['indexdef']
                }
                for row in rows
            ]
        except Exception as e:
            return [{"error": str(e)}]


def create_database_plugin(database_type: str, connection_string: str) -> DatabasePlugin:
    """
    Factory function to create the appropriate database plugin.
    
    Args:
        database_type: Type of database ('sqlserver', 'azuresynapse', 'postgresql')
        connection_string: Database connection string
        
    Returns:
        DatabasePlugin instance
        
    Raises:
        ValueError: If database_type is not supported
    """
    database_type = database_type.lower()
    
    if database_type == 'sqlserver':
        return SQLServerPlugin(connection_string)
    elif database_type == 'azuresynapse':
        return AzureSynapsePlugin(connection_string)
    elif database_type == 'postgresql':
        return PostgreSQLPlugin(connection_string)
    else:
        raise ValueError(f"Unsupported database type: {database_type}")