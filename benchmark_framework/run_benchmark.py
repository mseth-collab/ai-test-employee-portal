"""
Benchmark Runner Script
======================

This script provides a command-line interface for running SQL query benchmarks
with comprehensive configuration management and reporting capabilities.
"""

import asyncio
import json
import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the benchmark framework to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.benchmark_engine import BenchmarkEngine, BenchmarkQuery, BenchmarkConfig
from core.database import create_database_plugin
from analysis.flamegraph_analyzer import FlamegraphAnalyzer
from analysis.etp_analyzer import ETPAnalyzer


class BenchmarkRunner:
    """Main benchmark runner with configuration management."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the benchmark runner.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_configuration()
        self.database_plugin = None
        self.flamegraph_analyzer = FlamegraphAnalyzer()
        self.etp_analyzer = ETPAnalyzer()
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from file or create default configuration."""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # Return default configuration
        return {
            "database": {
                "type": "sqlserver",
                "connection_string": "",
                "timeout_seconds": 30
            },
            "benchmark": {
                "iterations": 5,
                "warmup_iterations": 2,
                "timeout_seconds": 300,
                "collect_detailed_metrics": True,
                "collect_execution_plan": True,
                "collect_query_statistics": True
            },
            "queries": [],
            "output": {
                "format": "json",
                "include_execution_plans": False,
                "include_flamegraph_analysis": False,
                "include_etp_analysis": False,
                "save_raw_results": True,
                "output_directory": "./benchmark_results"
            }
        }
    
    def _save_configuration(self, output_path: str):
        """Save current configuration to file."""
        with open(output_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    async def initialize_database(self) -> bool:
        """Initialize database connection."""
        try:
            db_config = self.config.get("database", {})
            db_type = db_config.get("type", "sqlserver")
            connection_string = db_config.get("connection_string", "")
            
            if not connection_string:
                print("❌ Error: Database connection string not configured")
                return False
            
            self.database_plugin = create_database_plugin(db_type, connection_string)
            
            if await self.database_plugin.connect():
                print(f"✅ Successfully connected to {db_type} database")
                return True
            else:
                print(f"❌ Failed to connect to {db_type} database")
                return False
        
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
    
    async def run_benchmark_from_config(self) -> Dict[str, Any]:
        """Run benchmark based on loaded configuration."""
        if not self.database_plugin:
            print("❌ Database not initialized")
            return {"error": "Database not initialized"}
        
        # Create benchmark engine
        engine = BenchmarkEngine(self.database_plugin)
        
        # Prepare benchmark configuration
        benchmark_config = BenchmarkConfig(
            name=self.config.get("name", "Benchmark Run"),
            description=self.config.get("description", ""),
            iterations=self.config["benchmark"]["iterations"],
            warmup_iterations=self.config["benchmark"]["warmup_iterations"],
            timeout_seconds=self.config["benchmark"]["timeout_seconds"],
            collect_detailed_metrics=self.config["benchmark"]["collect_detailed_metrics"],
            collect_execution_plan=self.config["benchmark"]["collect_execution_plan"],
            collect_query_statistics=self.config["benchmark"]["collect_query_statistics"]
        )
        
        # Load queries from configuration
        queries = []
        for query_config in self.config.get("queries", []):
            query = BenchmarkQuery(
                id=query_config["id"],
                name=query_config["name"],
                sql=query_config["sql"],
                category=query_config.get("category", "general"),
                expected_execution_time=query_config.get("expected_execution_time"),
                tags=query_config.get("tags", [])
            )
            queries.append(query)
        
        if not queries:
            print("❌ No queries configured for benchmark")
            return {"error": "No queries configured"}
        
        print(f"🚀 Starting benchmark with {len(queries)} queries")
        
        # Run benchmark suite
        results = await engine.run_benchmark_suite(queries, benchmark_config)
        
        # Generate report
        report = engine.generate_report(results)
        
        # Save results
        output_config = self.config.get("output", {})
        output_dir = Path(output_config.get("output_directory", "./benchmark_results"))
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        results_data = {
            "timestamp": timestamp,
            "config": self.config,
            "results": [self._serialize_result(result) for result in results],
            "summary": {
                "total_queries": len(results),
                "successful_runs": sum(1 for r in results if r.success),
                "failed_runs": sum(1 for r in results if not r.success)
            }
        }
        
        json_path = output_dir / f"benchmark_results_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        # Save text report
        report_path = output_dir / f"benchmark_report_{timestamp}.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"📄 Results saved to: {output_dir}")
        print(f"   - JSON results: {json_path.name}")
        print(f"   - Text report: {report_path.name}")
        
        # Additional analyses if enabled
        if output_config.get("include_flamegraph_analysis", False):
            await self._run_flamegraph_analysis(results, output_dir, timestamp)
        
        if output_config.get("include_etp_analysis", False):
            await self._run_etp_analysis(results, output_dir, timestamp)
        
        return results_data
    
    async def _run_flamegraph_analysis(self, results: List, output_dir: Path, timestamp: str):
        """Run flamegraph analysis on benchmark results."""
        print("🔥 Running flamegraph analysis...")
        
        # This would require flamegraph data from the benchmark
        # For now, we'll create a placeholder analysis
        flamegraph_report = "# Flamegraph Analysis Report\n\n"
        flamegraph_report += "Flamegraph analysis requires actual flamegraph data.\n"
        flamegraph_report += "This feature would analyze performance bottlenecks from profiling data.\n"
        
        flamegraph_path = output_dir / f"flamegraph_analysis_{timestamp}.txt"
        with open(flamegraph_path, 'w') as f:
            f.write(flamegraph_report)
        
        print(f"   Flamegraph analysis saved to: {flamegraph_path.name}")
    
    async def _run_etp_analysis(self, results: List, output_dir: Path, timestamp: str):
        """Run ETP analysis on benchmark results."""
        print("📊 Running ETP analysis...")
        
        # This would require ETP file data
        # For now, we'll create a placeholder analysis
        etp_report = "# ETP (Extended Events) Analysis Report\n\n"
        etp_report += "ETP analysis requires Extended Events trace files.\n"
        etp_report += "This feature would analyze SQL Server performance events.\n"
        
        etp_path = output_dir / f"etp_analysis_{timestamp}.txt"
        with open(etp_path, 'w') as f:
            f.write(etp_report)
        
        print(f"   ETP analysis saved to: {etp_path.name}")
    
    def _serialize_result(self, result) -> Dict[str, Any]:
        """Serialize benchmark result for JSON output."""
        return {
            "query_id": result.query_id,
            "query_name": result.query_name,
            "start_time": result.start_time.isoformat(),
            "end_time": result.end_time.isoformat(),
            "success": result.success,
            "error_message": result.error_message,
            "execution_times": result.execution_times,
            "mean_execution_time": result.mean_execution_time,
            "median_execution_time": result.median_execution_time,
            "std_deviation": result.std_deviation,
            "min_execution_time": result.min_execution_time,
            "max_execution_time": result.max_execution_time,
            "detailed_metrics": result.detailed_metrics,
            "execution_plan": result.execution_plan,
            "query_statistics": result.query_statistics
        }
    
    def create_sample_config(self, output_path: str):
        """Create a sample configuration file."""
        sample_config = {
            "name": "Sample SQL Query Benchmark",
            "description": "Sample benchmark configuration for SQL performance testing",
            "database": {
                "type": "sqlserver",
                "connection_string": "DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password",
                "timeout_seconds": 30
            },
            "benchmark": {
                "iterations": 5,
                "warmup_iterations": 2,
                "timeout_seconds": 300,
                "collect_detailed_metrics": True,
                "collect_execution_plan": True,
                "collect_query_statistics": True
            },
            "queries": [
                {
                    "id": "query_001",
                    "name": "Simple SELECT Query",
                    "sql": "SELECT * FROM [YourTable] WHERE [YourColumn] = 'value'",
                    "category": "select",
                    "expected_execution_time": 100.0,
                    "tags": ["basic", "select"]
                },
                {
                    "id": "query_002", 
                    "name": "Join Query",
                    "sql": "SELECT t1.*, t2.* FROM [Table1] t1 INNER JOIN [Table2] t2 ON t1.ID = t2.Table1ID WHERE t1.Date > '2023-01-01'",
                    "category": "join",
                    "expected_execution_time": 500.0,
                    "tags": ["join", "filter"]
                },
                {
                    "id": "query_003",
                    "name": "Aggregation Query", 
                    "sql": "SELECT [Category], COUNT(*), SUM([Amount]) FROM [Transactions] GROUP BY [Category] ORDER BY SUM([Amount]) DESC",
                    "category": "aggregation",
                    "expected_execution_time": 300.0,
                    "tags": ["aggregate", "groupby"]
                }
            ],
            "output": {
                "format": "json",
                "include_execution_plans": True,
                "include_flamegraph_analysis": False,
                "include_etp_analysis": False,
                "save_raw_results": True,
                "output_directory": "./benchmark_results"
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(sample_config, f, indent=2)
        
        print(f"✅ Sample configuration created: {output_path}")


async def main():
    """Main entry point for the benchmark runner."""
    parser = argparse.ArgumentParser(description="SQL Query Benchmark Runner")
    parser.add_argument("--config", "-c", help="Path to benchmark configuration file")
    parser.add_argument("--create-sample", "-s", help="Create sample configuration file at specified path")
    parser.add_argument("--validate-only", "-v", action="store_true", help="Only validate configuration without running benchmarks")
    
    args = parser.parse_args()
    
    # Create sample configuration if requested
    if args.create_sample:
        runner = BenchmarkRunner()
        runner.create_sample_config(args.create_sample)
        return
    
    # Initialize runner
    runner = BenchmarkRunner(args.config)
    
    # Validate configuration
    if not runner.config.get("database", {}).get("connection_string"):
        print("❌ Error: Database connection string not configured")
        if args.config:
            print(f"   Please update: {args.config}")
        else:
            print("   Please create a configuration file with database settings")
        return
    
    if args.validate_only:
        print("✅ Configuration validation completed")
        print(f"   Database type: {runner.config.get('database', {}).get('type', 'Unknown')}")
        print(f"   Query count: {len(runner.config.get('queries', []))}")
        print(f"   Iterations: {runner.config.get('benchmark', {}).get('iterations', 0)}")
        return
    
    # Initialize database
    if not await runner.initialize_database():
        return
    
    # Run benchmark
    try:
        results = await runner.run_benchmark_from_config()
        
        if "error" in results:
            print(f"❌ Benchmark failed: {results['error']}")
            sys.exit(1)
        
        # Print summary
        summary = results.get("summary", {})
        print(f"\n🎉 Benchmark completed!")
        print(f"   Total queries: {summary.get('total_queries', 0)}")
        print(f"   Successful: {summary.get('successful_runs', 0)}")
        print(f"   Failed: {summary.get('failed_runs', 0)}")
        
        if summary.get("failed_runs", 0) > 0:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        if runner.database_plugin:
            await runner.database_plugin.disconnect()


if __name__ == "__main__":
    asyncio.run(main())