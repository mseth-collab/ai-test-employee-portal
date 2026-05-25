"""
Metrics Dashboard Module
=======================

This module provides web-based visualization and dashboard capabilities for SQL query benchmark results,
including interactive charts, performance metrics display, and comprehensive reporting.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import base64


class MetricsDashboard:
    """Generates interactive web dashboards for benchmark results."""
    
    def __init__(self, output_directory: str = "./dashboard_output"):
        """
        Initialize the metrics dashboard generator.
        
        Args:
            output_directory: Directory to save dashboard files
        """
        self.output_dir = Path(output_directory)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_dashboard(self, benchmark_results: List[Dict[str, Any]], output_filename: str = "benchmark_dashboard.html") -> str:
        """
        Generate an interactive HTML dashboard for benchmark results.
        
        Args:
            benchmark_results: List of benchmark result dictionaries
            output_filename: Name of the output HTML file
            
        Returns:
            Path to the generated dashboard file
        """
        # Process results for visualization
        processed_data = self._process_results_for_dashboard(benchmark_results)
        
        # Generate HTML dashboard
        dashboard_html = self._generate_html_dashboard(processed_data)
        
        # Save dashboard
        dashboard_path = self.output_dir / output_filename
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        # Generate additional assets (CSS, JS)
        self._generate_dashboard_assets()
        
        return str(dashboard_path)
    
    def _process_results_for_dashboard(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process benchmark results for dashboard visualization."""
        processed = {
            "summary": {
                "total_queries": len(results),
                "successful_runs": 0,
                "failed_runs": 0,
                "total_executions": 0
            },
            "query_performance": [],
            "performance_trends": [],
            "comparison_data": [],
            "system_metrics": [],
            "execution_plans": [],
            "recommendations": []
        }
        
        for result in results:
            # Extract basic info
            query_name = result.get("query_name", "Unknown Query")
            query_id = result.get("query_id", "unknown")
            success = result.get("success", False)
            
            # Update summary
            if success:
                processed["summary"]["successful_runs"] += 1
            else:
                processed["summary"]["failed_runs"] += 1
            
            # Performance metrics
            execution_times = result.get("execution_times", [])
            processed["summary"]["total_executions"] += len(execution_times)
            
            if execution_times:
                mean_time = result.get("mean_execution_time", 0)
                median_time = result.get("median_execution_time", 0)
                min_time = result.get("min_execution_time", 0)
                max_time = result.get("max_execution_time", 0)
                std_dev = result.get("std_deviation", 0)
                
                processed["query_performance"].append({
                    "query_id": query_id,
                    "query_name": query_name,
                    "success": success,
                    "mean_time_ms": mean_time,
                    "median_time_ms": median_time,
                    "min_time_ms": min_time,
                    "max_time_ms": max_time,
                    "std_deviation_ms": std_dev,
                    "execution_times": execution_times,
                    "performance_score": self._calculate_performance_score(mean_time, std_dev, len(execution_times))
                })
            
            # System metrics
            detailed_metrics = result.get("detailed_metrics", {})
            if detailed_metrics:
                processed["system_metrics"].append({
                    "query_id": query_id,
                    "query_name": query_name,
                    "metrics": detailed_metrics
                })
            
            # Execution plans
            execution_plan = result.get("execution_plan")
            if execution_plan:
                processed["execution_plans"].append({
                    "query_id": query_id,
                    "query_name": query_name,
                    "execution_plan": execution_plan
                })
        
        # Generate trends and comparisons
        processed["performance_trends"] = self._generate_performance_trends(processed["query_performance"])
        processed["comparison_data"] = self._generate_comparison_data(processed["query_performance"])
        processed["recommendations"] = self._generate_dashboard_recommendations(processed["query_performance"])
        
        return processed
    
    def _generate_html_dashboard(self, data: Dict[str, Any]) -> str:
        """Generate the complete HTML dashboard."""
        
        # Convert data to JSON for JavaScript
        data_json = json.dumps(data, indent=2, default=str)
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Query Benchmark Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
    <style>
        {self._get_dashboard_css()}
    </style>
</head>
<body>
    <div class="container">
        <header class="dashboard-header">
            <h1>🗃️ SQL Query Benchmark Dashboard</h1>
            <p class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </header>

        <div class="dashboard-summary">
            {self._generate_summary_cards(data["summary"])}
        </div>

        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h2>📊 Query Performance Overview</h2>
                <canvas id="performanceChart" width="400" height="200"></canvas>
            </div>

            <div class="dashboard-card">
                <h2>📈 Performance Trends</h2>
                <canvas id="trendsChart" width="400" height="200"></canvas>
            </div>

            <div class="dashboard-card">
                <h2>⚡ Execution Time Distribution</h2>
                <canvas id="distributionChart" width="400" height="200"></canvas>
            </div>

            <div class="dashboard-card">
                <h2>🎯 Performance Comparison</h2>
                <canvas id="comparisonChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="dashboard-section">
            <h2>📋 Detailed Query Analysis</h2>
            <div class="query-details-table">
                {self._generate_query_details_table(data["query_performance"])}
            </div>
        </div>

        <div class="dashboard-section">
            <h2>💡 Optimization Recommendations</h2>
            <div class="recommendations">
                {self._generate_recommendations_section(data["recommendations"])}
            </div>
        </div>

        <div class="dashboard-section">
            <h2>🔍 System Metrics</h2>
            <div class="system-metrics">
                {self._generate_system_metrics_section(data["system_metrics"])}
            </div>
        </div>

        <div class="dashboard-section">
            <h2>📄 Execution Plans</h2>
            <div class="execution-plans">
                {self._generate_execution_plans_section(data["execution_plans"])}
            </div>
        </div>
    </div>

    <script>
        {self._get_dashboard_javascript(data_json)}
    </script>
</body>
</html>
        """
        
        return html_template.strip()
    
    def _generate_summary_cards(self, summary: Dict[str, Any]) -> str:
        """Generate summary cards HTML."""
        success_rate = (summary["successful_runs"] / summary["total_queries"] * 100) if summary["total_queries"] > 0 else 0
        
        cards = f"""
        <div class="summary-card">
            <h3>Total Queries</h3>
            <div class="metric-value">{summary["total_queries"]}</div>
        </div>
        <div class="summary-card success">
            <h3>Successful Runs</h3>
            <div class="metric-value">{summary["successful_runs"]}</div>
        </div>
        <div class="summary-card warning">
            <h3>Failed Runs</h3>
            <div class="metric-value">{summary["failed_runs"]}</div>
        </div>
        <div class="summary-card info">
            <h3>Success Rate</h3>
            <div class="metric-value">{success_rate:.1f}%</div>
        </div>
        <div class="summary-card">
            <h3>Total Executions</h3>
            <div class="metric-value">{summary["total_executions"]}</div>
        </div>
        """
        return cards
    
    def _generate_query_details_table(self, query_performance: List[Dict[str, Any]]) -> str:
        """Generate detailed query performance table."""
        if not query_performance:
            return "<p>No query performance data available.</p>"
        
        table_rows = []
        for query in query_performance:
            status_class = "success" if query["success"] else "failed"
            table_rows.append(f"""
            <tr class="{status_class}">
                <td>{query["query_name"]}</td>
                <td>{query["mean_time_ms"]:.2f} ms</td>
                <td>{query["median_time_ms"]:.2f} ms</td>
                <td>{query["min_time_ms"]:.2f} ms</td>
                <td>{query["max_time_ms"]:.2f} ms</td>
                <td>{query["std_deviation_ms"]:.2f} ms</td>
                <td>
                    <span class="performance-score score-{query["performance_score"]}">
                        {query["performance_score"].title()}
                    </span>
                </td>
            </tr>
            """)
        
        table_html = f"""
        <table class="query-table">
            <thead>
                <tr>
                    <th>Query Name</th>
                    <th>Mean Time</th>
                    <th>Median Time</th>
                    <th>Min Time</th>
                    <th>Max Time</th>
                    <th>Std Deviation</th>
                    <th>Performance Score</th>
                </tr>
            </thead>
            <tbody>
                {''.join(table_rows)}
            </tbody>
        </table>
        """
        return table_html
    
    def _generate_recommendations_section(self, recommendations: List[Dict[str, Any]]) -> str:
        """Generate recommendations section."""
        if not recommendations:
            return "<p>No specific recommendations available. System appears to be performing well.</p>"
        
        recommendation_cards = []
        for rec in recommendations:
            priority_class = rec.get("priority", "medium").lower()
            recommendation_cards.append(f"""
            <div class="recommendation-card priority-{priority_class}">
                <h4>{rec.get("category", "General")}</h4>
                <p>{rec.get("description", "No description available")}</p>
                <div class="recommendation-impact">
                    <span class="priority-badge">Priority: {rec.get("priority", "Medium")}</span>
                    <span class="impact-badge">Impact: {rec.get("impact", "Unknown")}</span>
                </div>
            </div>
            """)
        
        return ''.join(recommendation_cards)
    
    def _generate_system_metrics_section(self, system_metrics: List[Dict[str, Any]]) -> str:
        """Generate system metrics section."""
        if not system_metrics:
            return "<p>No system metrics available.</p>"
        
        metrics_sections = []
        for metrics_data in system_metrics:
            query_name = metrics_data.get("query_name", "Unknown Query")
            metrics = metrics_data.get("metrics", {})
            
            # Extract key metrics
            cpu_usage = metrics.get("cpu", {}).get("usage_percent", 0)
            memory_usage = metrics.get("memory", {}).get("used_percent", 0)
            
            metrics_sections.append(f"""
            <div class="metrics-card">
                <h4>{query_name}</h4>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <label>CPU Usage:</label>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {cpu_usage}%"></div>
                        </div>
                        <span>{cpu_usage:.1f}%</span>
                    </div>
                    <div class="metric-item">
                        <label>Memory Usage:</label>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {memory_usage}%"></div>
                        </div>
                        <span>{memory_usage:.1f}%</span>
                    </div>
                </div>
            </div>
            """)
        
        return ''.join(metrics_sections)
    
    def _generate_execution_plans_section(self, execution_plans: List[Dict[str, Any]]) -> str:
        """Generate execution plans section."""
        if not execution_plans:
            return "<p>No execution plans available.</p>"
        
        plan_sections = []
        for plan_data in execution_plans:
            query_name = plan_data.get("query_name", "Unknown Query")
            execution_plan = plan_data.get("execution_plan", "No execution plan available")
            
            # Truncate long execution plans
            if len(execution_plan) > 500:
                execution_plan = execution_plan[:500] + "..."
            
            plan_sections.append(f"""
            <div class="execution-plan-card">
                <h4>{query_name}</h4>
                <pre class="execution-plan">{execution_plan}</pre>
            </div>
            """)
        
        return ''.join(plan_sections)
    
    def _calculate_performance_score(self, mean_time: float, std_dev: float, sample_count: int) -> str:
        """Calculate performance score based on metrics."""
        # Simple scoring algorithm
        if mean_time < 100 and std_dev < 20:
            return "excellent"
        elif mean_time < 500 and std_dev < 50:
            return "good"
        elif mean_time < 1000 and std_dev < 100:
            return "fair"
        else:
            return "poor"
    
    def _generate_performance_trends(self, query_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate performance trend data."""
        # This would analyze performance over time if timestamp data was available
        # For now, return processed trends
        trends = []
        for query in query_performance:
            trends.append({
                "query_name": query["query_name"],
                "performance_score": query["performance_score"],
                "trend_direction": "stable"  # Placeholder
            })
        return trends
    
    def _generate_comparison_data(self, query_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate comparison data for charts."""
        return query_performance
    
    def _generate_dashboard_recommendations(self, query_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on query performance."""
        recommendations = []
        
        # Analyze poor performers
        poor_performers = [q for q in query_performance if q["performance_score"] == "poor"]
        if poor_performers:
            recommendations.append({
                "category": "Performance Optimization",
                "description": f"Found {len(poor_performers)} queries with poor performance. Consider optimization.",
                "priority": "high",
                "impact": "high"
            })
        
        # Analyze high variance
        high_variance = [q for q in query_performance if q["std_deviation_ms"] > q["mean_time_ms"] * 0.3]
        if high_variance:
            recommendations.append({
                "category": "Performance Stability",
                "description": f"Found {len(high_variance)} queries with high performance variance.",
                "priority": "medium",
                "impact": "medium"
            })
        
        return recommendations
    
    def _get_dashboard_css(self) -> str:
        """Get CSS styles for the dashboard."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .dashboard-header {
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
        }
        
        .dashboard-header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .timestamp {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .dashboard-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .summary-card.success {
            border-left-color: #4CAF50;
        }
        
        .summary-card.warning {
            border-left-color: #FF9800;
        }
        
        .summary-card.info {
            border-left-color: #2196F3;
        }
        
        .summary-card h3 {
            color: #666;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .dashboard-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .dashboard-card h2 {
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .dashboard-section {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .dashboard-section h2 {
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .query-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .query-table th,
        .query-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .query-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        
        .query-table tr.success {
            background-color: #f0f8f0;
        }
        
        .query-table tr.failed {
            background-color: #fff0f0;
        }
        
        .performance-score {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .score-excellent {
            background-color: #4CAF50;
            color: white;
        }
        
        .score-good {
            background-color: #8BC34A;
            color: white;
        }
        
        .score-fair {
            background-color: #FF9800;
            color: white;
        }
        
        .score-poor {
            background-color: #F44336;
            color: white;
        }
        
        .recommendations {
            display: grid;
            gap: 15px;
        }
        
        .recommendation-card {
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid;
        }
        
        .recommendation-card.priority-high {
            background-color: #fff5f5;
            border-left-color: #F44336;
        }
        
        .recommendation-card.priority-medium {
            background-color: #fffbf0;
            border-left-color: #FF9800;
        }
        
        .recommendation-card.priority-low {
            background-color: #f0f8ff;
            border-left-color: #2196F3;
        }
        
        .recommendation-card h4 {
            margin-bottom: 8px;
            color: #333;
        }
        
        .recommendation-impact {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .priority-badge,
        .impact-badge {
            background-color: #667eea;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        .metric-item {
            display: grid;
            grid-template-columns: 100px 1fr 50px;
            gap: 10px;
            align-items: center;
        }
        
        .progress-bar {
            background-color: #e0e0e0;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            background-color: #667eea;
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .execution-plan {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .dashboard-summary {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }
        """
    
    def _get_dashboard_javascript(self, data_json: str) -> str:
        """Get JavaScript code for dashboard charts and interactivity."""
        return f"""
        const dashboardData = {data_json};
        
        // Chart.js configurations
        const chartColors = {{
            primary: '#667eea',
            success: '#4CAF50',
            warning: '#FF9800',
            danger: '#F44336',
            info: '#2196F3'
        }};
        
        // Performance Overview Chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        const performanceData = dashboardData.query_performance.map(q => ({{
            x: q.query_name,
            y: q.mean_time_ms
        }}));
        
        new Chart(performanceCtx, {{
            type: 'bar',
            data: {{
                labels: dashboardData.query_performance.map(q => q.query_name),
                datasets: [{{
                    label: 'Mean Execution Time (ms)',
                    data: dashboardData.query_performance.map(q => q.mean_time_ms),
                    backgroundColor: chartColors.primary,
                    borderColor: chartColors.primary,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Execution Time (ms)'
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Performance Trends Chart
        const trendsCtx = document.getElementById('trendsChart').getContext('2d');
        new Chart(trendsCtx, {{
            type: 'line',
            data: {{
                labels: dashboardData.query_performance.map(q => q.query_name),
                datasets: [{{
                    label: 'Mean Time',
                    data: dashboardData.query_performance.map(q => q.mean_time_ms),
                    borderColor: chartColors.primary,
                    backgroundColor: chartColors.primary + '20',
                    fill: false
                }}, {{
                    label: 'Max Time',
                    data: dashboardData.query_performance.map(q => q.max_time_ms),
                    borderColor: chartColors.danger,
                    backgroundColor: chartColors.danger + '20',
                    fill: false
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Execution Time (ms)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Distribution Chart
        const distributionCtx = document.getElementById('distributionChart').getContext('2d');
        const distributionData = dashboardData.query_performance.map(q => q.execution_times).flat();
        
        new Chart(distributionCtx, {{
            type: 'histogram',
            data: {{
                labels: [], // Will be calculated
                datasets: [{{
                    label: 'Execution Time Distribution',
                    data: distributionData,
                    backgroundColor: chartColors.info,
                    borderColor: chartColors.info,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Frequency'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Execution Time (ms)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Performance Comparison Chart
        const comparisonCtx = document.getElementById('comparisonChart').getContext('2d');
        new Chart(comparisonCtx, {{
            type: 'radar',
            data: {{
                labels: ['Mean Time', 'Stability', 'Min Time', 'Max Time', 'Success Rate'],
                datasets: dashboardData.query_performance.map((q, index) => ({{
                    label: q.query_name,
                    data: [
                        (1000 - q.mean_time_ms) / 10, // Normalized
                        (100 - Math.min(q.std_deviation_ms * 2, 100)) / 100, // Stability score
                        (1000 - q.min_time_ms) / 10, // Normalized
                        (1000 - q.max_time_ms) / 10, // Normalized
                        q.success ? 100 : 0 // Success rate
                    ],
                    borderColor: Object.values(chartColors)[index % Object.values(chartColors).length],
                    backgroundColor: Object.values(chartColors)[index % Object.values(chartColors).length] + '20'
                }}))
            }},
            options: {{
                responsive: true,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // Initialize dashboard
        console.log('Dashboard initialized with', dashboardData.query_performance.length, 'queries');
        """
    
    def _generate_dashboard_assets(self):
        """Generate additional CSS and JS assets."""
        # For a more sophisticated setup, you could generate separate CSS/JS files
        # For now, everything is embedded in the HTML for simplicity
        pass


def create_sample_dashboard(output_path: str = "sample_dashboard.html"):
    """Create a sample dashboard with mock data."""
    # Generate sample benchmark results
    sample_results = [
        {
            "query_id": "query_001",
            "query_name": "Simple SELECT Query",
            "success": True,
            "mean_execution_time": 125.5,
            "median_execution_time": 120.0,
            "min_execution_time": 110.0,
            "max_execution_time": 150.0,
            "std_deviation": 15.2,
            "execution_times": [110, 120, 125, 130, 140, 135, 115, 145, 125, 120],
            "detailed_metrics": {
                "cpu": {"usage_percent": 45.2},
                "memory": {"used_percent": 62.1}
            },
            "execution_plan": "|--Table Scan (Table: Users, Rows: 10000, Cost: 0.28)"
        },
        {
            "query_id": "query_002",
            "query_name": "Join Query",
            "success": True,
            "mean_execution_time": 340.8,
            "median_execution_time": 335.0,
            "min_execution_time": 310.0,
            "max_execution_time": 400.0,
            "std_deviation": 28.4,
            "execution_times": [310, 320, 335, 340, 350, 345, 330, 360, 340, 325],
            "detailed_metrics": {
                "cpu": {"usage_percent": 78.5},
                "memory": {"used_percent": 84.3}
            },
            "execution_plan": "|--Nested Loops (Inner Join)\\n   |--Index Scan (Orders)\\n   |--Index Seek (Customers)"
        },
        {
            "query_id": "query_003",
            "query_name": "Aggregation Query",
            "success": True,
            "mean_execution_time": 890.2,
            "median_execution_time": 875.0,
            "min_execution_time": 820.0,
            "max_execution_time": 1050.0,
            "std_deviation": 67.1,
            "execution_times": [820, 850, 875, 890, 920, 900, 870, 940, 880, 860],
            "detailed_metrics": {
                "cpu": {"usage_percent": 92.1},
                "memory": {"used_percent": 95.7}
            },
            "execution_plan": "|--Sort\\n|--Hash Match (Aggregate)\\n   |--Table Scan (Transactions)"
        }
    ]
    
    # Create dashboard
    dashboard = MetricsDashboard()
    dashboard_path = dashboard.generate_dashboard(sample_results, output_path)
    
    print(f"✅ Sample dashboard created: {dashboard_path}")
    return dashboard_path


if __name__ == "__main__":
    # Create sample dashboard
    create_sample_dashboard()