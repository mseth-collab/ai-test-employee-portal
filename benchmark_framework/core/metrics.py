"""
Metrics Collection Module
========================

This module provides comprehensive metrics collection capabilities for SQL query performance analysis.
"""

import asyncio
import json
import psutil
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class MetricsCollector:
    """Collects comprehensive performance metrics during query execution."""
    
    def __init__(self, database_plugin):
        """
        Initialize the metrics collector.
        
        Args:
            database_plugin: Database-specific plugin for system metrics
        """
        self.database_plugin = database_plugin
        self.system_metrics_history = []
        self.start_time = None
    
    async def start_monitoring(self) -> str:
        """Start system and database monitoring."""
        self.start_time = datetime.now()
        
        # Start background monitoring task
        asyncio.create_task(self._background_monitoring())
        
        return f"Monitoring started at {self.start_time}"
    
    async def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return collected metrics."""
        if not self.start_time:
            return {"error": "Monitoring was not started"}
        
        end_time = datetime.now()
        monitoring_duration = (end_time - self.start_time).total_seconds()
        
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "monitoring_duration_seconds": monitoring_duration,
            "total_samples": len(self.system_metrics_history),
            "system_metrics": self.system_metrics_history.copy()
        }
    
    async def collect_detailed_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive performance metrics."""
        metrics = {}
        
        # System metrics
        metrics['system'] = await self._collect_system_metrics()
        
        # Database-specific metrics
        try:
            metrics['database'] = await self._collect_database_metrics()
        except Exception as e:
            metrics['database'] = {"error": str(e)}
        
        # Query execution metrics
        metrics['execution'] = await self._collect_execution_metrics()
        
        # Performance analysis
        metrics['analysis'] = await self._analyze_metrics(metrics)
        
        return metrics
    
    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level performance metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk I/O metrics
            disk_io = psutil.disk_io_counters()
            disk_usage = psutil.disk_usage('/')
            
            # Network metrics
            network_io = psutil.net_io_counters()
            
            # Process-specific metrics (if running as Python process)
            try:
                process = psutil.Process()
                process_memory = process.memory_info()
                process_cpu = process.cpu_percent()
            except:
                process_memory = {}
                process_cpu = 0
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": cpu_count,
                    "frequency_mhz": cpu_freq.current if cpu_freq else None
                },
                "memory": {
                    "total_gb": memory.total / (1024**3),
                    "available_gb": memory.available / (1024**3),
                    "used_percent": memory.percent,
                    "total_swap_gb": swap.total / (1024**3),
                    "used_swap_percent": swap.percent
                },
                "disk": {
                    "total_gb": disk_usage.total / (1024**3),
                    "free_gb": disk_usage.free / (1024**3),
                    "usage_percent": (disk_usage.used / disk_usage.total) * 100,
                    "read_bytes": disk_io.read_bytes if disk_io else 0,
                    "write_bytes": disk_io.write_bytes if disk_io else 0
                },
                "network": {
                    "bytes_sent": network_io.bytes_sent if network_io else 0,
                    "bytes_recv": network_io.bytes_recv if network_io else 0,
                    "packets_sent": network_io.packets_sent if network_io else 0,
                    "packets_recv": network_io.packets_recv if network_io else 0
                },
                "process": {
                    "memory_rss_mb": process_memory.rss / (1024**2) if hasattr(process_memory, 'rss') else 0,
                    "memory_vms_mb": process_memory.vms / (1024**2) if hasattr(process_memory, 'vms') else 0,
                    "cpu_percent": process_cpu
                }
            }
        except Exception as e:
            return {"error": f"Failed to collect system metrics: {e}"}
    
    async def _collect_database_metrics(self) -> Dict[str, Any]:
        """Collect database-specific performance metrics."""
        if not self.database_plugin:
            return {"error": "No database plugin available"}
        
        metrics = {}
        
        try:
            # System metrics from database
            system_metrics = await self.database_plugin.get_system_metrics()
            metrics['system_metrics'] = system_metrics
            
            # Table statistics
            table_stats = await self.database_plugin.get_table_statistics()
            metrics['table_statistics'] = table_stats
            
            # Index information
            index_info = await self.database_plugin.get_index_information()
            metrics['index_information'] = index_info
            
        except Exception as e:
            metrics['error'] = str(e)
        
        return metrics
    
    async def _collect_execution_metrics(self) -> Dict[str, Any]:
        """Collect query execution-specific metrics."""
        # This would be populated during actual query execution
        # For now, return placeholder structure
        
        return {
            "current_batch_size": 0,
            "average_batch_time": 0,
            "total_rows_processed": 0,
            "cache_hit_ratio": 0.0,
            "buffer_pool_usage": 0.0,
            "tempdb_usage": 0.0
        }
    
    async def _analyze_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collected metrics for performance insights."""
        analysis = {}
        
        try:
            # Analyze system metrics
            system_metrics = metrics.get('system', {})
            if system_metrics and 'error' not in system_metrics:
                cpu_usage = system_metrics.get('cpu', {}).get('usage_percent', 0)
                memory_usage = system_metrics.get('memory', {}).get('used_percent', 0)
                
                analysis['system_health'] = {
                    "cpu_usage_status": self._get_usage_status(cpu_usage),
                    "memory_usage_status": self._get_usage_status(memory_usage),
                    "overall_system_load": "high" if max(cpu_usage, memory_usage) > 80 else "normal"
                }
            
            # Analyze database metrics
            db_metrics = metrics.get('database', {})
            if db_metrics and 'error' not in db_metrics:
                analysis['database_health'] = self._analyze_database_health(db_metrics)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(metrics)
            
        except Exception as e:
            analysis['error'] = f"Failed to analyze metrics: {e}"
        
        return analysis
    
    def _get_usage_status(self, usage_percent: float) -> str:
        """Get status string based on usage percentage."""
        if usage_percent > 90:
            return "critical"
        elif usage_percent > 75:
            return "high"
        elif usage_percent > 50:
            return "moderate"
        else:
            return "normal"
    
    def _analyze_database_health(self, db_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze database health from metrics."""
        health = {}
        
        # Check table statistics
        table_stats = db_metrics.get('table_statistics', [])
        if isinstance(table_stats, list) and table_stats and 'error' not in table_stats[0]:
            # Analyze table sizes and suggest optimization
            large_tables = [t for t in table_stats if t.get('row_count', 0) > 1000000]
            
            health['table_analysis'] = {
                "total_tables": len(table_stats),
                "large_tables_count": len(large_tables),
                "large_tables": [t.get('table', 'unknown') for t in large_tables[:5]]  # Top 5
            }
        
        # Check index information
        index_info = db_metrics.get('index_information', [])
        if isinstance(index_info, list) and index_info and 'error' not in index_info[0]:
            heap_tables = [i for i in index_info if i.get('index_type') == 'HEAP']
            
            health['index_analysis'] = {
                "total_indexes": len(index_info),
                "heap_tables_count": len(heap_tables),
                "heap_tables": [i.get('table', 'unknown') for i in heap_tables[:5]]
            }
        
        return health
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on metrics."""
        recommendations = []
        
        try:
            system_metrics = metrics.get('system', {})
            if system_metrics and 'error' not in system_metrics:
                cpu_usage = system_metrics.get('cpu', {}).get('usage_percent', 0)
                memory_usage = system_metrics.get('memory', {}).get('used_percent', 0)
                
                if cpu_usage > 80:
                    recommendations.append("High CPU usage detected. Consider query optimization or additional indexing.")
                
                if memory_usage > 85:
                    recommendations.append("High memory usage detected. Consider optimizing memory-intensive queries or adding RAM.")
            
            db_metrics = metrics.get('database', {})
            if db_metrics and 'error' not in db_metrics:
                # Check for heap tables
                index_info = db_metrics.get('index_information', [])
                if isinstance(index_info, list) and index_info and 'error' not in index_info[0]:
                    heap_tables = [i for i in index_info if i.get('index_type') == 'HEAP']
                    if heap_tables:
                        recommendations.append(f"Found {len(heap_tables)} heap tables. Consider adding appropriate indexes.")
                
                # Check table statistics
                table_stats = db_metrics.get('table_statistics', [])
                if isinstance(table_stats, list) and table_stats and 'error' not in table_stats[0]:
                    very_large_tables = [t for t in table_stats if t.get('row_count', 0) > 10000000]
                    if very_large_tables:
                        recommendations.append(f"Found {len(very_large_tables)} very large tables. Consider partitioning or archival strategies.")
        
        except Exception as e:
            recommendations.append(f"Error generating recommendations: {e}")
        
        if not recommendations:
            recommendations.append("System appears to be operating normally.")
        
        return recommendations
    
    async def _background_monitoring(self):
        """Background task to continuously collect system metrics."""
        while self.start_time and self._should_continue_monitoring():
            try:
                metrics = await self._collect_system_metrics()
                self.system_metrics_history.append(metrics)
                
                # Keep only recent samples to limit memory usage
                if len(self.system_metrics_history) > 100:
                    self.system_metrics_history.pop(0)
                
                # Sleep between samples (every 5 seconds)
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Error in background monitoring: {e}")
                await asyncio.sleep(10)  # Wait longer on error
    
    def _should_continue_monitoring(self) -> bool:
        """Check if background monitoring should continue."""
        # This could be enhanced with proper stop signals
        # For now, just check if we've been running for a reasonable time
        if not self.start_time:
            return False
        
        duration = (datetime.now() - self.start_time).total_seconds()
        return duration < 3600  # Stop after 1 hour


class QueryExecutionMetrics:
    """Tracks metrics during actual query execution."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.records_read = 0
        self.records_written = 0
        self.memory_used = 0
        self.tempdb_used = 0
        self.logical_reads = 0
        self.physical_reads = 0
        self.spills_to_disk = 0
        
    def start_execution(self):
        """Mark the start of query execution."""
        self.start_time = time.perf_counter()
    
    def end_execution(self):
        """Mark the end of query execution."""
        self.end_time = time.perf_counter()
    
    def get_execution_time_ms(self) -> float:
        """Get execution time in milliseconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get all metrics as a dictionary."""
        return {
            "execution_time_ms": self.get_execution_time_ms(),
            "records_read": self.records_read,
            "records_written": self.records_written,
            "memory_used_kb": self.memory_used,
            "tempdb_used_kb": self.tempdb_used,
            "logical_reads": self.logical_reads,
            "physical_reads": self.physical_reads,
            "spills_to_disk": self.spills_to_disk,
            "read_write_ratio": self.records_read / max(self.records_written, 1)
        }