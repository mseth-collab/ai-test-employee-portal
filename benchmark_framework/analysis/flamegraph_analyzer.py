"""
Flamegraph Analysis Module
=========================

This module provides flamegraph generation and analysis capabilities for SQL query performance profiling.
It supports parsing various flamegraph formats and extracting performance insights.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics


@dataclass
class FlamegraphNode:
    """Represents a node in the flamegraph tree."""
    name: str
    value: float  # Execution time in milliseconds
    children: List['FlamegraphNode']
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class FlamegraphAnalyzer:
    """Analyzes flamegraph data for performance bottlenecks and optimization opportunities."""
    
    def __init__(self):
        self.supported_formats = ['collapsed_stack', 'd3_flamegraph', 'speedscope', 'custom']
        self.analysis_cache = {}
    
    def parse_flamegraph(self, data: str, format_type: str = 'collapsed_stack') -> Optional[FlamegraphNode]:
        """
        Parse flamegraph data into a tree structure.
        
        Args:
            data: Flamegraph data as string
            format_type: Format of the data ('collapsed_stack', 'd3_flamegraph', 'speedscope', 'custom')
            
        Returns:
            Root node of the flamegraph tree
        """
        try:
            if format_type == 'collapsed_stack':
                return self._parse_collapsed_stack(data)
            elif format_type == 'd3_flamegraph':
                return self._parse_d3_flamegraph(json.loads(data))
            elif format_type == 'speedscope':
                return self._parse_speedscope(json.loads(data))
            elif format_type == 'custom':
                return self._parse_custom_format(data)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
        except Exception as e:
            print(f"Failed to parse flamegraph: {e}")
            return None
    
    def analyze_bottlenecks(self, root: FlamegraphNode) -> Dict[str, Any]:
        """
        Analyze flamegraph tree to identify performance bottlenecks.
        
        Args:
            root: Root node of the flamegraph tree
            
        Returns:
            Dictionary containing bottleneck analysis
        """
        if not root:
            return {"error": "Invalid flamegraph data"}
        
        # Calculate total execution time
        total_time = self._calculate_total_time(root)
        
        # Find hot paths (most time consuming)
        hot_paths = self._find_hot_paths(root, top_k=10)
        
        # Find functions with highest self-time
        self_time_analysis = self._analyze_self_time(root)
        
        # Analyze call patterns
        call_patterns = self._analyze_call_patterns(root)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(root, hot_paths)
        
        return {
            "total_execution_time_ms": total_time,
            "analysis_timestamp": datetime.now().isoformat(),
            "hot_paths": hot_paths,
            "self_time_analysis": self_time_analysis,
            "call_patterns": call_patterns,
            "optimization_opportunities": optimization_opportunities,
            "flamegraph_stats": self._calculate_flamegraph_stats(root)
        }
    
    def compare_flamegraphs(self, baseline_root: FlamegraphNode, comparison_root: FlamegraphNode) -> Dict[str, Any]:
        """
        Compare two flamegraphs to identify performance changes.
        
        Args:
            baseline_root: Baseline flamegraph root
            comparison_root: Comparison flamegraph root
            
        Returns:
            Dictionary containing comparison analysis
        """
        baseline_analysis = self.analyze_bottlenecks(baseline_root)
        comparison_analysis = self.analyze_bottlenecks(comparison_root)
        
        # Extract key metrics for comparison
        baseline_total = baseline_analysis.get("total_execution_time_ms", 0)
        comparison_total = comparison_analysis.get("total_execution_time_ms", 0)
        
        # Calculate performance changes
        total_change = comparison_total - baseline_total
        total_change_percent = (total_change / baseline_total * 100) if baseline_total > 0 else 0
        
        # Compare hot paths
        hot_path_changes = self._compare_hot_paths(
            baseline_analysis.get("hot_paths", []),
            comparison_analysis.get("hot_paths", [])
        )
        
        # Identify regression and improvement areas
        regressions = self._identify_regressions(baseline_analysis, comparison_analysis)
        improvements = self._identify_improvements(baseline_analysis, comparison_analysis)
        
        return {
            "comparison_timestamp": datetime.now().isoformat(),
            "baseline_total_time_ms": baseline_total,
            "comparison_total_time_ms": comparison_total,
            "total_change_ms": total_change,
            "total_change_percent": total_change_percent,
            "performance_change_classification": self._classify_performance_change(total_change_percent),
            "hot_path_changes": hot_path_changes,
            "regressions": regressions,
            "improvements": improvements,
            "net_performance_impact": self._calculate_net_performance_impact(regressions, improvements)
        }
    
    def generate_optimization_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable optimization report from flamegraph analysis."""
        report = []
        
        report.append("# Flamegraph Performance Analysis Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Overall performance summary
        total_time = analysis.get("total_execution_time_ms", 0)
        report.append("## Overall Performance")
        report.append(f"- Total execution time: {total_time:.2f} ms")
        
        flamegraph_stats = analysis.get("flamegraph_stats", {})
        if flamegraph_stats:
            report.append(f"- Unique functions: {flamegraph_stats.get('unique_functions', 'Unknown')}")
            report.append(f"- Call depth: {flamegraph_stats.get('max_depth', 'Unknown')}")
            report.append(f"- Call count: {flamegraph_stats.get('total_calls', 'Unknown')}")
        report.append("")
        
        # Hot paths analysis
        hot_paths = analysis.get("hot_paths", [])
        if hot_paths:
            report.append("## Performance Hot Paths")
            report.append("Top 10 most time-consuming call paths:")
            report.append("")
            for i, path in enumerate(hot_paths, 1):
                function_name = path.get("function", "Unknown")
                self_time = path.get("self_time", 0)
                total_time = path.get("total_time", 0)
                percentage = (self_time / total_time * 100) if total_time > 0 else 0
                
                report.append(f"{i}. **{function_name}**")
                report.append(f"   - Self time: {self_time:.2f} ms ({percentage:.1f}%)")
                report.append(f"   - Total time: {total_time:.2f} ms")
                report.append(f"   - Calls: {path.get('call_count', 0)}")
                report.append("")
        
        # Self-time analysis
        self_time_analysis = analysis.get("self_time_analysis", {})
        if self_time_analysis:
            report.append("## Functions with Highest Self-Time")
            top_self_time = self_time_analysis.get("top_functions", [])
            for i, func in enumerate(top_self_time[:5], 1):
                name = func.get("function", "Unknown")
                self_time = func.get("self_time", 0)
                report.append(f"{i}. {name}: {self_time:.2f} ms")
            report.append("")
        
        # Optimization opportunities
        opportunities = analysis.get("optimization_opportunities", [])
        if opportunities:
            report.append("## Optimization Opportunities")
            for i, opp in enumerate(opportunities, 1):
                category = opp.get("category", "General")
                function_name = opp.get("function", "Unknown")
                potential_saving = opp.get("potential_saving_ms", 0)
                recommendation = opp.get("recommendation", "No specific recommendation")
                
                report.append(f"{i}. **{category}: {function_name}**")
                report.append(f"   - Potential time saving: {potential_saving:.2f} ms")
                report.append(f"   - Recommendation: {recommendation}")
                report.append("")
        
        return "\n".join(report)
    
    def _parse_collapsed_stack(self, data: str) -> FlamegraphNode:
        """Parse collapsed stack format (common for perf/FlameGraph tool)."""
        lines = data.strip().split('\n')
        root = FlamegraphNode("root", 0, [], {})
        
        for line in lines:
            if not line.strip():
                continue
            
            # Parse format: stack_pattern value
            parts = line.rsplit(' ', 1)
            if len(parts) != 2:
                continue
            
            stack = parts[0]
            try:
                value = float(parts[1])
            except ValueError:
                continue
            
            # Parse stack frames
            frames = stack.split(';')
            if not frames or frames[-1].strip() == '':
                continue
            
            # Build tree
            current = root
            for frame in frames:
                frame = frame.strip()
                if not frame:
                    continue
                
                # Find or create child
                child = None
                for c in current.children:
                    if c.name == frame:
                        child = c
                        break
                
                if not child:
                    child = FlamegraphNode(frame, 0, [], {})
                    current.children.append(child)
                
                current = child
            
            # Add value to leaf node
            current.value += value
        
        return root
    
    def _parse_d3_flamegraph(self, data: Dict[str, Any]) -> FlamegraphNode:
        """Parse D3.js flamegraph JSON format."""
        # This would require implementing the specific D3 flamegraph format
        # For now, return a simple placeholder implementation
        return FlamegraphNode("d3_flamegraph", 0, [], {"format": "d3"})
    
    def _parse_speedscope(self, data: Dict[str, Any]) -> FlamegraphNode:
        """Parse Speedscope JSON format."""
        # This would require implementing the Speedscope format
        # For now, return a simple placeholder implementation
        return FlamegraphNode("speedscope", 0, [], {"format": "speedscope"})
    
    def _parse_custom_format(self, data: str) -> FlamegraphNode:
        """Parse custom flamegraph format."""
        # This would be customized based on specific flamegraph source
        return FlamegraphNode("custom", 0, [], {"format": "custom"})
    
    def _calculate_total_time(self, node: FlamegraphNode) -> float:
        """Calculate total execution time for a node including children."""
        total = node.value
        for child in node.children:
            total += self._calculate_total_time(child)
        return total
    
    def _find_hot_paths(self, node: FlamegraphNode, top_k: int = 10) -> List[Dict[str, Any]]:
        """Find the hottest (most time-consuming) execution paths."""
        hot_paths = []
        
        def traverse(node: FlamegraphNode, current_path: List[str], current_time: float):
            path_with_node = current_path + [node.name]
            total_time = self._calculate_total_time(node)
            
            # For leaf nodes or significant nodes, add to hot paths
            if not node.children or total_time > 0:
                hot_paths.append({
                    "path": path_with_node,
                    "function": node.name,
                    "total_time": total_time,
                    "self_time": node.value,
                    "call_count": self._estimate_call_count(node),
                    "level": len(path_with_node)
                })
            
            # Continue traversal
            for child in node.children:
                traverse(child, path_with_node, current_time)
        
        traverse(node, [], 0)
        
        # Sort by total time and return top k
        hot_paths.sort(key=lambda x: x["total_time"], reverse=True)
        return hot_paths[:top_k]
    
    def _analyze_self_time(self, root: FlamegraphNode) -> Dict[str, Any]:
        """Analyze functions by their self-time (time spent in the function itself)."""
        self_time_data = []
        
        def collect_self_time(node: FlamegraphNode):
            # Calculate self-time (value excluding children's time)
            children_time = sum(self._calculate_total_time(child) for child in node.children)
            self_time = node.value
            total_time = self_time + children_time
            
            if total_time > 0:  # Only include functions that actually executed
                self_time_data.append({
                    "function": node.name,
                    "self_time": self_time,
                    "total_time": total_time,
                    "self_time_percentage": (self_time / total_time * 100) if total_time > 0 else 0,
                    "call_count": self._estimate_call_count(node)
                })
            
            # Recursively analyze children
            for child in node.children:
                collect_self_time(child)
        
        collect_self_time(root)
        
        # Sort by self-time
        self_time_data.sort(key=lambda x: x["self_time"], reverse=True)
        
        return {
            "total_functions": len(self_time_data),
            "top_functions": self_time_data[:10],
            "self_time_distribution": self._calculate_time_distribution(self_time_data)
        }
    
    def _analyze_call_patterns(self, root: FlamegraphNode) -> Dict[str, Any]:
        """Analyze calling patterns and relationships."""
        call_graph = {}
        
        def build_call_graph(node: FlamegraphNode, parent: Optional[str] = None):
            function_name = node.name
            
            if function_name not in call_graph:
                call_graph[function_name] = {
                    "callees": {},
                    "callers": set(),
                    "total_calls": 0,
                    "total_time": 0
                }
            
            call_graph[function_name]["total_calls"] += 1
            call_graph[function_name]["total_time"] += node.value
            
            if parent:
                call_graph[function_name]["callers"].add(parent)
            
            # Process children
            for child in node.children:
                child_name = child.name
                if child_name not in call_graph[function_name]["callees"]:
                    call_graph[function_name]["callees"][child_name] = 0
                call_graph[function_name]["callees"][child_name] += 1
                
                build_call_graph(child, function_name)
        
        build_call_graph(root)
        
        # Convert sets to lists for JSON serialization
        for func_data in call_graph.values():
            func_data["callers"] = list(func_data["callers"])
        
        return {
            "call_graph": call_graph,
            "most_called_functions": self._find_most_called_functions(call_graph),
            "deepest_call_chains": self._find_deepest_chains(root)
        }
    
    def _identify_optimization_opportunities(self, root: FlamegraphNode, hot_paths: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities."""
        opportunities = []
        
        # Analyze hot paths for optimization
        for path in hot_paths[:5]:  # Focus on top 5 hot paths
            function_name = path["function"]
            total_time = path["total_time"]
            
            # Database-specific optimization suggestions
            if self._is_sql_function(function_name):
                if "scan" in function_name.lower():
                    opportunities.append({
                        "category": "Index Optimization",
                        "function": function_name,
                        "current_time_ms": total_time,
                        "potential_saving_ms": total_time * 0.3,  # Assume 30% improvement possible
                        "recommendation": "Consider adding appropriate indexes to reduce table scans"
                    })
                elif "join" in function_name.lower():
                    opportunities.append({
                        "category": "Join Optimization",
                        "function": function_name,
                        "current_time_ms": total_time,
                        "potential_saving_ms": total_time * 0.25,
                        "recommendation": "Review join order and consider using hash joins or appropriate indexes"
                    })
            
            # General optimization patterns
            if total_time > 100:  # Functions taking more than 100ms
                opportunities.append({
                    "category": "Performance Critical",
                    "function": function_name,
                    "current_time_ms": total_time,
                    "potential_saving_ms": total_time * 0.15,
                    "recommendation": "Consider algorithmic optimization or caching for high-time functions"
                })
        
        return opportunities
    
    def _compare_hot_paths(self, baseline_hot_paths: List[Dict], comparison_hot_paths: List[Dict]) -> List[Dict[str, Any]]:
        """Compare hot paths between baseline and comparison."""
        changes = []
        
        # Create dictionaries for easy lookup
        baseline_dict = {path["function"]: path for path in baseline_hot_paths}
        comparison_dict = {path["function"]: path for path in comparison_hot_paths}
        
        # Find new functions in comparison
        new_functions = set(comparison_dict.keys()) - set(baseline_dict.keys())
        for func in new_functions:
            changes.append({
                "function": func,
                "change_type": "new_function",
                "time_ms": comparison_dict[func]["total_time"],
                "impact": "negative" if comparison_dict[func]["total_time"] > 10 else "minimal"
            })
        
        # Find disappeared functions
        disappeared_functions = set(baseline_dict.keys()) - set(comparison_dict.keys())
        for func in disappeared_functions:
            changes.append({
                "function": func,
                "change_type": "function_removed",
                "time_ms": baseline_dict[func]["total_time"],
                "impact": "positive"
            })
        
        # Find changed functions
        common_functions = set(baseline_dict.keys()) & set(comparison_dict.keys())
        for func in common_functions:
            baseline_time = baseline_dict[func]["total_time"]
            comparison_time = comparison_dict[func]["total_time"]
            change = comparison_time - baseline_time
            change_percent = (change / baseline_time * 100) if baseline_time > 0 else 0
            
            if abs(change_percent) > 10:  # Significant change (>10%)
                changes.append({
                    "function": func,
                    "change_type": "time_change",
                    "baseline_time_ms": baseline_time,
                    "comparison_time_ms": comparison_time,
                    "change_ms": change,
                    "change_percent": change_percent,
                    "impact": "negative" if change > 0 else "positive"
                })
        
        return changes
    
    def _identify_regressions(self, baseline: Dict, comparison: Dict) -> List[Dict[str, Any]]:
        """Identify performance regressions."""
        regressions = []
        
        # Check for new hot paths
        baseline_hot = {path["function"] for path in baseline.get("hot_paths", [])}
        comparison_hot = {path["function"] for path in comparison.get("hot_paths", [])}
        
        new_hot_paths = comparison_hot - baseline_hot
        for func in new_hot_paths:
            path_data = next((p for p in comparison.get("hot_paths", []) if p["function"] == func), None)
            if path_data and path_data["total_time"] > 50:  # Significant new hot path
                regressions.append({
                    "type": "new_hot_path",
                    "function": func,
                    "time_ms": path_data["total_time"],
                    "severity": "high" if path_data["total_time"] > 200 else "medium"
                })
        
        # Check for increased execution times
        for baseline_path in baseline.get("hot_paths", []):
            func_name = baseline_path["function"]
            comparison_path = next((p for p in comparison.get("hot_paths", []) if p["function"] == func_name), None)
            
            if comparison_path:
                baseline_time = baseline_path["total_time"]
                comparison_time = comparison_path["total_time"]
                
                if comparison_time > baseline_time * 1.2:  # 20% increase
                    regressions.append({
                        "type": "time_increase",
                        "function": func_name,
                        "baseline_time_ms": baseline_time,
                        "comparison_time_ms": comparison_time,
                        "increase_ms": comparison_time - baseline_time,
                        "severity": "high" if comparison_time > baseline_time * 1.5 else "medium"
                    })
        
        return regressions
    
    def _identify_improvements(self, baseline: Dict, comparison: Dict) -> List[Dict[str, Any]]:
        """Identify performance improvements."""
        improvements = []
        
        # Check for reduced execution times
        for baseline_path in baseline.get("hot_paths", []):
            func_name = baseline_path["function"]
            comparison_path = next((p for p in comparison.get("hot_paths", []) if p["function"] == func_name), None)
            
            if comparison_path:
                baseline_time = baseline_path["total_time"]
                comparison_time = comparison_path["total_time"]
                
                if comparison_time < baseline_time * 0.8:  # 20% decrease
                    improvement_ms = baseline_time - comparison_time
                    improvements.append({
                        "type": "time_reduction",
                        "function": func_name,
                        "baseline_time_ms": baseline_time,
                        "comparison_time_ms": comparison_time,
                        "improvement_ms": improvement_ms,
                        "improvement_percent": (improvement_ms / baseline_time * 100) if baseline_time > 0 else 0
                    })
        
        return improvements
    
    def _calculate_net_performance_impact(self, regressions: List[Dict], improvements: List[Dict]) -> Dict[str, Any]:
        """Calculate net performance impact of changes."""
        total_regression_ms = sum(r.get("time_ms", 0) for r in regressions) + \
                             sum(r.get("increase_ms", 0) for r in regressions if "increase_ms" in r)
        
        total_improvement_ms = sum(i.get("improvement_ms", 0) for i in improvements)
        
        net_impact_ms = total_improvement_ms - total_regression_ms
        
        return {
            "total_regression_ms": total_regression_ms,
            "total_improvement_ms": total_improvement_ms,
            "net_impact_ms": net_impact_ms,
            "net_impact_classification": "positive" if net_impact_ms < 0 else "negative" if net_impact_ms > 0 else "neutral"
        }
    
    def _calculate_flamegraph_stats(self, root: FlamegraphNode) -> Dict[str, Any]:
        """Calculate basic statistics about the flamegraph."""
        stats = {
            "unique_functions": 0,
            "max_depth": 0,
            "total_calls": 0,
            "total_unique_stacks": 0
        }
        
        def traverse(node: FlamegraphNode, depth: int):
            stats["unique_functions"] += 1
            stats["max_depth"] = max(stats["max_depth"], depth)
            stats["total_calls"] += 1
            
            for child in node.children:
                traverse(child, depth + 1)
        
        traverse(root, 0)
        
        return stats
    
    def _estimate_call_count(self, node: FlamegraphNode) -> int:
        """Estimate call count based on node characteristics."""
        # This is a simplification - real flamegraphs would have call count data
        if node.value > 0:
            return max(1, int(node.value / 10))  # Rough estimate
        return 1
    
    def _calculate_time_distribution(self, self_time_data: List[Dict]) -> Dict[str, Any]:
        """Calculate time distribution statistics."""
        if not self_time_data:
            return {"distribution": "no_data"}
        
        self_times = [item["self_time"] for item in self_time_data]
        total_self_time = sum(self_times)
        
        # Calculate distribution percentiles
        sorted_times = sorted(self_times)
        n = len(sorted_times)
        
        return {
            "total_self_time_ms": total_self_time,
            "p50_ms": sorted_times[n // 2] if n > 0 else 0,
            "p90_ms": sorted_times[int(n * 0.9)] if n > 0 else 0,
            "p99_ms": sorted_times[int(n * 0.99)] if n > 0 else 0,
            "distribution": "skewed" if sorted_times[int(n * 0.9)] > sorted_times[int(n * 0.5)] * 3 else "normal"
        }
    
    def _find_most_called_functions(self, call_graph: Dict) -> List[Dict[str, Any]]:
        """Find the most frequently called functions."""
        function_stats = []
        for func_name, func_data in call_graph.items():
            function_stats.append({
                "function": func_name,
                "call_count": func_data["total_calls"],
                "total_time_ms": func_data["total_time"],
                "callee_count": len(func_data["callees"]),
                "caller_count": len(func_data["callers"])
            })
        
        function_stats.sort(key=lambda x: x["call_count"], reverse=True)
        return function_stats[:10]
    
    def _find_deepest_chains(self, root: FlamegraphNode, max_chains: int = 5) -> List[List[str]]:
        """Find the deepest call chains in the flamegraph."""
        chains = []
        
        def find_chains(node: FlamegraphNode, current_chain: List[str]):
            chain_with_node = current_chain + [node.name]
            
            if not node.children:  # Leaf node
                chains.append(chain_with_node)
            else:
                for child in node.children:
                    find_chains(child, chain_with_node)
        
        find_chains(root, [])
        
        # Sort by length and return deepest chains
        chains.sort(key=len, reverse=True)
        return chains[:max_chains]
    
    def _is_sql_function(self, function_name: str) -> bool:
        """Check if a function is SQL-related."""
        sql_keywords = ['scan', 'join', 'sort', 'aggregate', 'hash', 'merge', 'index', 'table', 'filter', 'select']
        function_lower = function_name.lower()
        return any(keyword in function_lower for keyword in sql_keywords)
    
    def _classify_performance_change(self, change_percent: float) -> str:
        """Classify the magnitude of performance change."""
        abs_change = abs(change_percent)
        if abs_change < 2:
            return "negligible"
        elif abs_change < 10:
            return "minor"
        elif abs_change < 25:
            return "moderate"
        else:
            return "significant"