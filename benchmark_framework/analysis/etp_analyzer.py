"""
ETP (Extended Events) Processing Module
=====================================

This module provides comprehensive ETP (Extended Events Trace) file processing and analysis capabilities
for SQL Server performance diagnostics and optimization.
"""

import xml.etree.ElementTree as ET
import json
import gzip
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics


@dataclass
class ETPEvent:
    """Represents a single Extended Events event."""
    timestamp: datetime
    name: str
    event_class: int
    cpu_time: Optional[float] = None
    duration: Optional[float] = None
    logical_reads: Optional[int] = None
    physical_reads: Optional[int] = None
    writes: Optional[int] = None
    row_count: Optional[int] = None
    text_data: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}


class ETPAnalyzer:
    """Analyzes Extended Events Trace (ETP) files for performance insights."""
    
    def __init__(self):
        self.supported_extensions = ['.xel', '.xem', '.xml', '.etl']
        self.event_cache = {}
        self.analysis_cache = {}
    
    def parse_etp_file(self, file_path: str) -> List[ETPEvent]:
        """
        Parse ETP file and extract events.
        
        Args:
            file_path: Path to the ETP file
            
        Returns:
            List of parsed ETPEvent objects
        """
        try:
            # Handle different file formats
            if file_path.endswith('.xel') or file_path.endswith('.xem'):
                return self._parse_xel_file(file_path)
            elif file_path.endswith('.xml'):
                return self._parse_xml_file(file_path)
            elif file_path.endswith('.etl'):
                return self._parse_etl_file(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            print(f"Failed to parse ETP file: {e}")
            return []
    
    def analyze_etp_events(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """
        Analyze ETP events for performance patterns and bottlenecks.
        
        Args:
            events: List of ETPEvent objects
            
        Returns:
            Dictionary containing comprehensive analysis
        """
        if not events:
            return {"error": "No events provided for analysis"}
        
        # Basic event statistics
        event_stats = self._analyze_event_statistics(events)
        
        # Performance analysis
        performance_analysis = self._analyze_performance_patterns(events)
        
        # Query analysis
        query_analysis = self._analyze_queries(events)
        
        # Resource usage analysis
        resource_analysis = self._analyze_resource_usage(events)
        
        # Time-based analysis
        temporal_analysis = self._analyze_temporal_patterns(events)
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(events)
        
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_events": len(events),
            "event_statistics": event_stats,
            "performance_analysis": performance_analysis,
            "query_analysis": query_analysis,
            "resource_analysis": resource_analysis,
            "temporal_analysis": temporal_analysis,
            "bottlenecks": bottlenecks,
            "summary": self._generate_etp_summary(event_stats, performance_analysis, bottlenecks)
        }
    
    def compare_etp_sessions(self, baseline_events: List[ETPEvent], comparison_events: List[ETPEvent]) -> Dict[str, Any]:
        """
        Compare two ETP sessions to identify performance changes.
        
        Args:
            baseline_events: Events from baseline session
            comparison_events: Events from comparison session
            
        Returns:
            Dictionary containing comparison analysis
        """
        baseline_analysis = self.analyze_etp_events(baseline_events)
        comparison_analysis = self.analyze_etp_events(comparison_events)
        
        # Compare overall performance metrics
        performance_comparison = self._compare_performance_metrics(baseline_analysis, comparison_analysis)
        
        # Compare resource usage
        resource_comparison = self._compare_resource_usage(baseline_analysis, comparison_analysis)
        
        # Compare temporal patterns
        temporal_comparison = self._compare_temporal_patterns(baseline_analysis, comparison_analysis)
        
        # Identify performance regressions
        regressions = self._identify_etp_regressions(baseline_analysis, comparison_analysis)
        
        # Identify improvements
        improvements = self._identify_etp_improvements(baseline_analysis, comparison_analysis)
        
        return {
            "comparison_timestamp": datetime.now().isoformat(),
            "baseline_total_events": len(baseline_events),
            "comparison_total_events": len(comparison_events),
            "performance_comparison": performance_comparison,
            "resource_comparison": resource_comparison,
            "temporal_comparison": temporal_comparison,
            "regressions": regressions,
            "improvements": improvements,
            "net_impact": self._calculate_net_etp_impact(regressions, improvements)
        }
    
    def generate_etp_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive ETP analysis report."""
        report = []
        
        report.append("# Extended Events (ETP) Performance Analysis Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary
        total_events = analysis.get("total_events", 0)
        summary = analysis.get("summary", {})
        
        report.append("## Executive Summary")
        report.append(f"- Total events analyzed: {total_events:,}")
        report.append(f"- Analysis period: {summary.get('analysis_period', 'Unknown')}")
        report.append(f"- Performance trend: {summary.get('performance_trend', 'Unknown')}")
        report.append("")
        
        # Event statistics
        event_stats = analysis.get("event_statistics", {})
        if event_stats:
            report.append("## Event Statistics")
            report.append(f"- Unique event types: {event_stats.get('unique_event_types', 0)}")
            report.append(f"- Most common event: {event_stats.get('most_common_event', 'Unknown')}")
            report.append(f"- Event rate: {event_stats.get('events_per_minute', 0):.1f} events/minute")
            report.append("")
        
        # Performance analysis
        performance = analysis.get("performance_analysis", {})
        if performance:
            report.append("## Performance Analysis")
            
            avg_duration = performance.get("average_duration_ms", 0)
            max_duration = performance.get("max_duration_ms", 0)
            p95_duration = performance.get("p95_duration_ms", 0)
            
            report.append(f"- Average query duration: {avg_duration:.2f} ms")
            report.append(f"- Maximum query duration: {max_duration:.2f} ms")
            report.append(f"- 95th percentile duration: {p95_duration:.2f} ms")
            
            slow_queries = performance.get("slow_queries", [])
            if slow_queries:
                report.append(f"- Queries longer than 1 second: {len(slow_queries)}")
            report.append("")
        
        # Resource analysis
        resource = analysis.get("resource_analysis", {})
        if resource:
            report.append("## Resource Usage")
            
            total_reads = resource.get("total_logical_reads", 0)
            total_physical_reads = resource.get("total_physical_reads", 0)
            total_writes = resource.get("total_writes", 0)
            
            report.append(f"- Total logical reads: {total_reads:,}")
            report.append(f"- Total physical reads: {total_physical_reads:,}")
            report.append(f"- Total writes: {total_writes:,}")
            report.append("")
        
        # Bottlenecks
        bottlenecks = analysis.get("bottlenecks", [])
        if bottlenecks:
            report.append("## Identified Bottlenecks")
            for i, bottleneck in enumerate(bottlenecks[:5], 1):
                category = bottleneck.get("category", "Unknown")
                description = bottleneck.get("description", "No description")
                impact = bottleneck.get("impact", "Unknown")
                
                report.append(f"{i}. **{category}**")
                report.append(f"   - Description: {description}")
                report.append(f"   - Impact: {impact}")
                report.append("")
        
        # Recommendations
        recommendations = self._generate_etp_recommendations(analysis)
        if recommendations:
            report.append("## Recommendations")
            for i, rec in enumerate(recommendations, 1):
                recommendation = rec.get("recommendation", "No recommendation")
                priority = rec.get("priority", "Unknown")
                
                report.append(f"{i}. [{priority}] {recommendation}")
            report.append("")
        
        return "\n".join(report)
    
    def _parse_xel_file(self, file_path: str) -> List[ETPEvent]:
        """Parse SQL Server Extended Events .xel file."""
        # This is a simplified implementation
        # Real implementation would use sqlserver.xevent package or similar
        events = []
        
        try:
            with open(file_path, 'rb') as f:
                # Read XEL file header and events
                # This would require understanding XEL file format
                # For now, return empty list with note
                print("XEL file parsing requires additional dependencies")
                return events
        except Exception as e:
            print(f"Error reading XEL file: {e}")
            return events
    
    def _parse_xml_file(self, file_path: str) -> List[ETPEvent]:
        """Parse Extended Events XML file."""
        events = []
        
        try:
            # Check if file is compressed
            if file_path.endswith('.xml.gz'):
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    content = f.read()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Parse XML
            root = ET.fromstring(content)
            
            # Define namespace
            ns = {'event': 'http://schemas.microsoft.com/sqlserver/2008/07/extendedevents'}
            
            # Extract events
            for event_elem in root.findall('.//event:event', ns):
                event = self._parse_event_element(event_elem, ns)
                if event:
                    events.append(event)
        
        except Exception as e:
            print(f"Error parsing XML file: {e}")
        
        return events
    
    def _parse_etl_file(self, file_path: str) -> List[ETPEvent]:
        """Parse Extended Events ETL file."""
        # ETL files are binary format, more complex to parse
        # This is a placeholder implementation
        print("ETL file parsing requires specialized tools")
        return []
    
    def _parse_event_element(self, event_elem: ET.Element, ns: Dict[str, str]) -> Optional[ETPEvent]:
        """Parse individual event element from XML."""
        try:
            # Extract basic event information
            name = event_elem.get('name', '')
            event_class = int(event_elem.get('id', 0))
            
            # Extract timestamp
            timestamp_str = event_elem.get('timestamp', '')
            if timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                timestamp = datetime.now()
            
            # Extract event data
            event_data = {}
            for data_elem in event_elem.findall('.//event:data', ns):
                key = data_elem.get('name', '')
                value = data_elem.get('value', '')
                
                # Convert numeric values
                if key in ['cpu_time', 'duration']:
                    try:
                        event_data[key] = float(value)
                    except ValueError:
                        event_data[key] = None
                elif key in ['logical_reads', 'physical_reads', 'writes', 'row_count']:
                    try:
                        event_data[key] = int(value)
                    except ValueError:
                        event_data[key] = None
                else:
                    event_data[key] = value
            
            # Create ETPEvent object
            return ETPEvent(
                timestamp=timestamp,
                name=name,
                event_class=event_class,
                cpu_time=event_data.get('cpu_time'),
                duration=event_data.get('duration'),
                logical_reads=event_data.get('logical_reads'),
                physical_reads=event_data.get('physical_reads'),
                writes=event_data.get('writes'),
                row_count=event_data.get('row_count'),
                text_data=event_data.get('text_data'),
                additional_data={k: v for k, v in event_data.items() if k not in [
                    'cpu_time', 'duration', 'logical_reads', 'physical_reads', 'writes', 'row_count', 'text_data'
                ]}
            )
        
        except Exception as e:
            print(f"Error parsing event element: {e}")
            return None
    
    def _analyze_event_statistics(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """Analyze basic event statistics."""
        if not events:
            return {}
        
        # Count event types
        event_types = {}
        for event in events:
            event_types[event.name] = event_types.get(event.name, 0) + 1
        
        # Calculate time span
        timestamps = [event.timestamp for event in events]
        time_span = max(timestamps) - min(timestamps)
        time_span_minutes = time_span.total_seconds() / 60
        
        # Most common event
        most_common = max(event_types.items(), key=lambda x: x[1]) if event_types else ("Unknown", 0)
        
        return {
            "unique_event_types": len(event_types),
            "most_common_event": most_common[0],
            "most_common_count": most_common[1],
            "event_type_distribution": event_types,
            "analysis_period": f"{time_span_minutes:.1f} minutes",
            "events_per_minute": len(events) / max(time_span_minutes, 1),
            "time_range": {
                "start": min(timestamps).isoformat(),
                "end": max(timestamps).isoformat(),
                "duration_seconds": time_span.total_seconds()
            }
        }
    
    def _analyze_performance_patterns(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """Analyze performance patterns from events."""
        durations = []
        cpu_times = []
        slow_queries = []
        
        for event in events:
            if event.duration is not None:
                durations.append(event.duration)
                
                # Categorize slow queries
                if event.duration > 1000:  # > 1 second
                    slow_queries.append({
                        "timestamp": event.timestamp.isoformat(),
                        "event_name": event.name,
                        "duration_ms": event.duration,
                        "text_data": event.text_data
                    })
            
            if event.cpu_time is not None:
                cpu_times.append(event.cpu_time)
        
        if not durations:
            return {"error": "No duration data available"}
        
        # Calculate statistics
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        min_duration = min(durations)
        
        # Calculate percentiles
        sorted_durations = sorted(durations)
        n = len(sorted_durations)
        p50_duration = sorted_durations[n // 2] if n > 0 else 0
        p95_duration = sorted_durations[int(n * 0.95)] if n > 0 else 0
        p99_duration = sorted_durations[int(n * 0.99)] if n > 0 else 0
        
        return {
            "average_duration_ms": avg_duration,
            "max_duration_ms": max_duration,
            "min_duration_ms": min_duration,
            "p50_duration_ms": p50_duration,
            "p95_duration_ms": p95_duration,
            "p99_duration_ms": p99_duration,
            "duration_std_dev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "slow_queries": slow_queries,
            "cpu_time_statistics": {
                "average_cpu_ms": statistics.mean(cpu_times) if cpu_times else 0,
                "max_cpu_ms": max(cpu_times) if cpu_times else 0
            }
        }
    
    def _analyze_queries(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """Analyze query patterns from events."""
        queries = {}
        
        for event in events:
            if event.text_data and event.name in ['sql_statement_completed', 'sql_batch_completed']:
                # Clean up query text
                query_text = event.text_data.strip()
                if len(query_text) > 100:
                    query_text = query_text[:100] + "..."
                
                if query_text not in queries:
                    queries[query_text] = {
                        "count": 0,
                        "total_duration": 0,
                        "total_cpu": 0,
                        "avg_duration": 0,
                        "max_duration": 0
                    }
                
                queries[query_text]["count"] += 1
                if event.duration:
                    queries[query_text]["total_duration"] += event.duration
                    queries[query_text]["max_duration"] = max(
                        queries[query_text]["max_duration"], event.duration
                    )
                if event.cpu_time:
                    queries[query_text]["total_cpu"] += event.cpu_time
        
        # Calculate averages
        for query_data in queries.values():
            if query_data["count"] > 0:
                query_data["avg_duration"] = query_data["total_duration"] / query_data["count"]
        
        # Find most frequent and slowest queries
        most_frequent = sorted(queries.items(), key=lambda x: x[1]["count"], reverse=True)[:5]
        slowest = sorted(queries.items(), key=lambda x: x[1]["max_duration"], reverse=True)[:5]
        
        return {
            "unique_queries": len(queries),
            "most_frequent_queries": [
                {
                    "query": query,
                    "count": data["count"],
                    "avg_duration_ms": data["avg_duration"]
                }
                for query, data in most_frequent
            ],
            "slowest_queries": [
                {
                    "query": query,
                    "max_duration_ms": data["max_duration"],
                    "avg_duration_ms": data["avg_duration"]
                }
                for query, data in slowest
            ]
        }
    
    def _analyze_resource_usage(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """Analyze resource usage patterns."""
        total_logical_reads = 0
        total_physical_reads = 0
        total_writes = 0
        total_rows = 0
        
        resource_heavy_events = []
        
        for event in events:
            if event.logical_reads:
                total_logical_reads += event.logical_reads
                if event.logical_reads > 10000:  # High I/O event
                    resource_heavy_events.append({
                        "timestamp": event.timestamp.isoformat(),
                        "event_name": event.name,
                        "logical_reads": event.logical_reads,
                        "physical_reads": event.physical_reads,
                        "duration_ms": event.duration
                    })
            
            if event.physical_reads:
                total_physical_reads += event.physical_reads
            
            if event.writes:
                total_writes += event.writes
            
            if event.row_count:
                total_rows += event.row_count
        
        return {
            "total_logical_reads": total_logical_reads,
            "total_physical_reads": total_physical_reads,
            "total_writes": total_writes,
            "total_rows_processed": total_rows,
            "average_logical_reads_per_event": total_logical_reads / len(events) if events else 0,
            "resource_heavy_events": resource_heavy_events,
            "cache_hit_ratio": (total_logical_reads - total_physical_reads) / max(total_logical_reads, 1)
        }
    
    def _analyze_temporal_patterns(self, events: List[ETPEvent]) -> Dict[str, Any]:
        """Analyze temporal patterns in events."""
        if not events:
            return {}
        
        # Group events by hour
        hourly_distribution = {}
        daily_distribution = {}
        
        for event in events:
            hour = event.timestamp.hour
            day = event.timestamp.strftime('%Y-%m-%d')
            
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
            daily_distribution[day] = daily_distribution.get(day, 0) + 1
        
        # Find peak hours
        peak_hour = max(hourly_distribution.items(), key=lambda x: x[1]) if hourly_distribution else (0, 0)
        
        # Find peak days
        peak_day = max(daily_distribution.items(), key=lambda x: x[1]) if daily_distribution else ("", 0)
        
        return {
            "hourly_distribution": hourly_distribution,
            "daily_distribution": daily_distribution,
            "peak_hour": peak_hour[0],
            "peak_hour_count": peak_hour[1],
            "peak_day": peak_day[0],
            "peak_day_count": peak_day[1]
        }
    
    def _identify_bottlenecks(self, events: List[ETPEvent]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks from events."""
        bottlenecks = []
        
        # Analyze duration patterns
        durations = [event.duration for event in events if event.duration]
        if durations:
            avg_duration = statistics.mean(durations)
            max_duration = max(durations)
            
            if max_duration > avg_duration * 5:  # Significantly slower than average
                bottlenecks.append({
                    "category": "Query Performance",
                    "description": f"Maximum query duration ({max_duration:.2f}ms) is significantly higher than average ({avg_duration:.2f}ms)",
                    "impact": "high",
                    "suggested_action": "Investigate slow-running queries and optimize them"
                })
        
        # Analyze I/O patterns
        high_io_events = [event for event in events if event.logical_reads and event.logical_reads > 50000]
        if high_io_events:
            bottlenecks.append({
                "category": "I/O Performance",
                "description": f"Found {len(high_io_events)} events with high logical reads (>50,000)",
                "impact": "medium",
                "suggested_action": "Consider adding indexes or optimizing queries to reduce I/O"
            })
        
        # Analyze CPU patterns
        high_cpu_events = [event for event in events if event.cpu_time and event.cpu_time > 1000]
        if high_cpu_events:
            bottlenecks.append({
                "category": "CPU Performance",
                "description": f"Found {len(high_cpu_events)} events with high CPU usage (>1000ms)",
                "impact": "medium",
                "suggested_action": "Optimize CPU-intensive queries or consider hardware upgrades"
            })
        
        return bottlenecks
    
    def _generate_etp_summary(self, event_stats: Dict, performance: Dict, bottlenecks: List[Dict]) -> Dict[str, Any]:
        """Generate summary of ETP analysis."""
        # Determine performance trend based on bottlenecks
        high_impact_bottlenecks = [b for b in bottlenecks if b.get("impact") == "high"]
        
        if len(high_impact_bottlenecks) > 2:
            performance_trend = "degrading"
        elif len(high_impact_bottlenecks) > 0:
            performance_trend = "concerning"
        else:
            performance_trend = "stable"
        
        return {
            "performance_trend": performance_trend,
            "critical_issues": len(high_impact_bottlenecks),
            "total_bottlenecks": len(bottlenecks),
            "analysis_period": event_stats.get("analysis_period", "Unknown")
        }
    
    def _compare_performance_metrics(self, baseline: Dict, comparison: Dict) -> Dict[str, Any]:
        """Compare performance metrics between baseline and comparison."""
        baseline_perf = baseline.get("performance_analysis", {})
        comparison_perf = comparison.get("performance_analysis", {})
        
        baseline_avg = baseline_perf.get("average_duration_ms", 0)
        comparison_avg = comparison_perf.get("average_duration_ms", 0)
        
        change_ms = comparison_avg - baseline_avg
        change_percent = (change_ms / baseline_avg * 100) if baseline_avg > 0 else 0
        
        return {
            "baseline_avg_duration_ms": baseline_avg,
            "comparison_avg_duration_ms": comparison_avg,
            "change_ms": change_ms,
            "change_percent": change_percent,
            "performance_change_classification": self._classify_etp_performance_change(change_percent)
        }
    
    def _compare_resource_usage(self, baseline: Dict, comparison: Dict) -> Dict[str, Any]:
        """Compare resource usage between baseline and comparison."""
        baseline_res = baseline.get("resource_analysis", {})
        comparison_res = comparison.get("resource_analysis", {})
        
        baseline_reads = baseline_res.get("total_logical_reads", 0)
        comparison_reads = comparison_res.get("total_logical_reads", 0)
        
        reads_change = comparison_reads - baseline_reads
        reads_change_percent = (reads_change / baseline_reads * 100) if baseline_reads > 0 else 0
        
        return {
            "baseline_total_reads": baseline_reads,
            "comparison_total_reads": comparison_reads,
            "reads_change": reads_change,
            "reads_change_percent": reads_change_percent
        }
    
    def _compare_temporal_patterns(self, baseline: Dict, comparison: Dict) -> Dict[str, Any]:
        """Compare temporal patterns between baseline and comparison."""
        # Simplified temporal comparison
        baseline_temp = baseline.get("temporal_analysis", {})
        comparison_temp = comparison.get("temporal_analysis", {})
        
        return {
            "baseline_peak_hour": baseline_temp.get("peak_hour", 0),
            "comparison_peak_hour": comparison_temp.get("peak_hour", 0),
            "peak_hour_change": comparison_temp.get("peak_hour", 0) - baseline_temp.get("peak_hour", 0)
        }
    
    def _identify_etp_regressions(self, baseline: Dict, comparison: Dict) -> List[Dict[str, Any]]:
        """Identify performance regressions from ETP analysis."""
        regressions = []
        
        perf_change = self._compare_performance_metrics(baseline, comparison)
        if perf_change.get("change_percent", 0) > 20:  # 20% degradation
            regressions.append({
                "type": "performance_degradation",
                "description": f"Performance degraded by {perf_change['change_percent']:.1f}%",
                "severity": "high" if perf_change["change_percent"] > 50 else "medium"
            })
        
        resource_change = self._compare_resource_usage(baseline, comparison)
        if resource_change.get("reads_change_percent", 0) > 30:  # 30% increase in reads
            regressions.append({
                "type": "resource_increase",
                "description": f"Logical reads increased by {resource_change['reads_change_percent']:.1f}%",
                "severity": "medium"
            })
        
        return regressions
    
    def _identify_etp_improvements(self, baseline: Dict, comparison: Dict) -> List[Dict[str, Any]]:
        """Identify performance improvements from ETP analysis."""
        improvements = []
        
        perf_change = self._compare_performance_metrics(baseline, comparison)
        if perf_change.get("change_percent", 0) < -20:  # 20% improvement
            improvements.append({
                "type": "performance_improvement",
                "description": f"Performance improved by {abs(perf_change['change_percent']):.1f}%",
                "improvement_percent": abs(perf_change["change_percent"])
            })
        
        return improvements
    
    def _calculate_net_etp_impact(self, regressions: List[Dict], improvements: List[Dict]) -> Dict[str, Any]:
        """Calculate net performance impact."""
        # Simplified impact calculation
        regression_severity = sum(1 for r in regressions if r.get("severity") == "high")
        improvement_count = len(improvements)
        
        if regression_severity > improvement_count:
            net_impact = "negative"
        elif improvement_count > regression_severity:
            net_impact = "positive"
        else:
            net_impact = "neutral"
        
        return {
            "net_impact": net_impact,
            "regression_count": len(regressions),
            "improvement_count": len(improvements)
        }
    
    def _generate_etp_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on ETP analysis."""
        recommendations = []
        
        # Performance-based recommendations
        performance = analysis.get("performance_analysis", {})
        if performance.get("slow_queries"):
            recommendations.append({
                "recommendation": "Optimize slow-running queries identified in the analysis",
                "priority": "high"
            })
        
        # Resource-based recommendations
        resource = analysis.get("resource_analysis", {})
        cache_hit_ratio = resource.get("cache_hit_ratio", 1.0)
        if cache_hit_ratio < 0.8:  # Less than 80% cache hit ratio
            recommendations.append({
                "recommendation": "Improve buffer cache efficiency - consider adding indexes or optimizing queries",
                "priority": "medium"
            })
        
        # Bottleneck-based recommendations
        bottlenecks = analysis.get("bottlenecks", [])
        for bottleneck in bottlenecks:
            if bottleneck.get("category") == "Query Performance":
                recommendations.append({
                    "recommendation": bottleneck.get("suggested_action", "Investigate query performance issues"),
                    "priority": "high"
                })
        
        return recommendations
    
    def _classify_etp_performance_change(self, change_percent: float) -> str:
        """Classify performance change magnitude for ETP analysis."""
        abs_change = abs(change_percent)
        if abs_change < 5:
            return "negligible"
        elif abs_change < 20:
            return "minor"
        elif abs_change < 50:
            return "moderate"
        else:
            return "significant"