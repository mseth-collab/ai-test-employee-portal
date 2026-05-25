"""
SQL Query Benchmark Framework - Core Engine
==========================================

This module provides the core benchmarking engine that orchestrates query execution,
performance measurement, and metrics collection across multiple database platforms.
"""

import time
import json
import asyncio
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics
import uuid

# Import with proper database plugin
from .database import DatabasePlugin

# Create minimal fallback classes for development
class MetricsCollector:
    def __init__(self, database_plugin):
        self.database_plugin = database_plugin
    
    async def collect_detailed_metrics(self):
        return {"warning": "Metrics collector not fully implemented"}

class PerformanceAnalyzer:
    def analyze_execution_times(self, times: List[float]):
        return {
            "mean": sum(times) / len(times) if times else 0,
            "median": 0,
            "std_dev": 0,
            "total_samples": len(times)
        }


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs."""
    name: str
    description: str = ""
    iterations: int = 5
    warmup_iterations: int = 2
    timeout_seconds: int = 300
    collect_detailed_metrics: bool = True
    collect_execution_plan: bool = True
    collect_query_statistics: bool = True
    run_with_distributed_execution: bool = False


@dataclass
class BenchmarkQuery:
    """Represents a single query to be benchmarked."""
    id: str
    name: str
    sql: str
    category: str = "general"
    expected_execution_time: Optional[float] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    query_id: str
    query_name: str
    start_time: datetime
    end_time: datetime
    success: bool
    error_message: Optional[str] = None
    
    # Execution metrics
    execution_times: Optional[List[float]] = None  # All iteration times in milliseconds
    mean_execution_time: float = 0.0
    median_execution_time: float = 0.0
    std_deviation: float = 0.0
    min_execution_time: float = 0.0
    max_execution_time: float = 0.0
    
    # Detailed metrics
    detailed_metrics: Optional[Dict[str, Any]] = None
    execution_plan: Optional[str] = None
    query_statistics: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.execution_times is None:
            self.execution_times = []
        
        if self.execution_times:
            self.mean_execution_time = statistics.mean(self.execution_times)
            self.median_execution_time = statistics.median(self.execution_times)
            self.std_deviation = statistics.stdev(self.execution_times) if len(self.execution_times) > 1 else 0.0
            self.min_execution_time = min(self.execution_times)
            self.max_execution_time = max(self.execution_times)


class BenchmarkEngine:
    """Main benchmark engine that orchestrates query execution and measurement."""
    
    def __init__(self, database_plugin: DatabasePlugin):
        """
        Initialize the benchmark engine.
        
        Args:
            database_plugin: Database-specific plugin for execution and metrics
        """
        self.database_plugin = database_plugin
        self.metrics_collector = MetricsCollector(database_plugin)
        self.performance_analyzer = PerformanceAnalyzer()
        
    async def run_benchmark(
        self, 
        query: BenchmarkQuery, 
        config: BenchmarkConfig
    ) -> BenchmarkResult:
        """
        Execute a single query benchmark with comprehensive metrics collection.
        
        Args:
            query: Query to benchmark
            config: Benchmark configuration
            
        Returns:
            BenchmarkResult with all collected metrics
        """
        result_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        print(f"🚀 Starting benchmark for query: {query.name}")
        print(f"   Query ID: {query.id}")
        print(f"   Iterations: {config.iterations}")
        print(f"   Warmup iterations: {config.warmup_iterations}")
        
        # Initialize result container
        result = BenchmarkResult(
            query_id=query.id,
            query_name=query.name,
            start_time=start_time,
            end_time=start_time,  # Will update later
            success=False
        )
        
        try:
            # Warmup runs (not included in final metrics)
            if config.warmup_iterations > 0:
                print(f"🔥 Performing {config.warmup_iterations} warmup iterations...")
                await self._execute_warmup_runs(query, config)
            
            # Main benchmark iterations
            print(f"📊 Running {config.iterations} benchmark iterations...")
            execution_times = []
            
            for iteration in range(config.iterations):
                print(f"   Iteration {iteration + 1}/{config.iterations}")
                
                iteration_start = time.perf_counter()
                
                # Execute query with optional distributed execution
                if config.run_with_distributed_execution:
                    success = await self._execute_distributed_query(query)
                else:
                    success = await self._execute_single_query(query)
                
                iteration_end = time.perf_counter()
                execution_time_ms = (iteration_end - iteration_start) * 1000
                
                execution_times.append(execution_time_ms)
                
                if not success:
                    raise Exception(f"Query execution failed in iteration {iteration + 1}")
            
            # Collect detailed metrics if requested
            detailed_metrics = None
            execution_plan = None
            query_statistics = None
            
            if config.collect_detailed_metrics:
                detailed_metrics = await self.metrics_collector.collect_detailed_metrics()
            
            if config.collect_execution_plan:
                execution_plan = await self.database_plugin.get_execution_plan(query.sql)
                
            if config.collect_query_statistics:
                query_statistics = await self.database_plugin.get_query_statistics(query.sql)
            
            # Update result with collected data
            result.execution_times = execution_times
            result.detailed_metrics = detailed_metrics
            result.execution_plan = execution_plan
            result.query_statistics = query_statistics
            result.success = True
            
        except Exception as e:
            result.error_message = str(e)
            print(f"❌ Benchmark failed: {e}")
        
        result.end_time = datetime.now()
        
        # Analyze performance if we have data
        if result.success and result.execution_times:
            analysis = self.performance_analyzer.analyze_execution_times(result.execution_times)
            result.detailed_metrics = result.detailed_metrics or {}
            result.detailed_metrics['performance_analysis'] = analysis
            
        print(f"✅ Benchmark completed for {query.name}")
        return result
    
    async def run_benchmark_suite(
        self, 
        queries: List[BenchmarkQuery], 
        config: BenchmarkConfig
    ) -> List[BenchmarkResult]:
        """
        Run multiple queries as a benchmark suite.
        
        Args:
            queries: List of queries to benchmark
            config: Benchmark configuration
            
        Returns:
            List of BenchmarkResult objects
        """
        print(f"🏃‍♂️ Starting benchmark suite with {len(queries)} queries")
        print(f"   Suite name: {config.name}")
        print(f"   Description: {config.description}")
        
        results = []
        
        for query in queries:
            result = await self.run_benchmark(query, config)
            results.append(result)
            
            # Add delay between queries to avoid resource contention
            if query != queries[-1]:  # Don't delay after last query
                await asyncio.sleep(1)
        
        print(f"🎉 Benchmark suite completed!")
        return results
    
    async def _execute_single_query(self, query: BenchmarkQuery) -> bool:
        """Execute a single query."""
        try:
            await self.database_plugin.execute_query(query.sql)
            return True
        except Exception as e:
            print(f"   ❌ Query execution failed: {e}")
            return False
    
    async def _execute_distributed_query(self, query: BenchmarkQuery) -> bool:
        """Execute query with distributed execution (placeholder for future implementation)."""
        # TODO: Implement distributed query execution
        return await self._execute_single_query(query)
    
    async def _execute_warmup_runs(self, query: BenchmarkQuery, config: BenchmarkConfig):
        """Execute warmup runs to stabilize query performance."""
        for i in range(config.warmup_iterations):
            try:
                await self.database_plugin.execute_query(query.sql)
            except Exception as e:
                print(f"   ⚠️ Warmup iteration {i + 1} failed: {e}")
    
    def generate_report(self, results: List[BenchmarkResult]) -> str:
        """Generate a comprehensive benchmark report."""
        report = []
        
        report.append("# SQL Query Benchmark Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Total queries benchmarked: {len(results)}")
        report.append(f"Successful runs: {sum(1 for r in results if r.success)}")
        report.append("")
        
        # Summary statistics
        successful_results = [r for r in results if r.success]
        if successful_results:
            all_execution_times = []
            for result in successful_results:
                if result.execution_times:
                    all_execution_times.extend(result.execution_times)
            
            if all_execution_times:
                report.append("## Overall Performance Summary")
                report.append(f"- Total executions: {len(all_execution_times)}")
                report.append(f"- Mean execution time: {statistics.mean(all_execution_times):.2f} ms")
                report.append(f"- Median execution time: {statistics.median(all_execution_times):.2f} ms")
                report.append(f"- Min execution time: {min(all_execution_times):.2f} ms")
                report.append(f"- Max execution time: {max(all_execution_times):.2f} ms")
                report.append("")
        
        # Individual query results
        report.append("## Query Performance Details")
        report.append("")
        
        for result in successful_results:
            report.append(f"### {result.query_name}")
            report.append(f"- Query ID: {result.query_id}")
            report.append(f"- Mean execution time: {result.mean_execution_time:.2f} ms")
            report.append(f"- Median execution time: {result.median_execution_time:.2f} ms")
            report.append(f"- Standard deviation: {result.std_deviation:.2f} ms")
            report.append(f"- Min/Max: {result.min_execution_time:.2f} / {result.max_execution_time:.2f} ms")
            report.append(f"- Iterations: {len(result.execution_times) if result.execution_times else 0}")
            report.append("")
        
        # Failed queries
        failed_results = [r for r in results if not r.success]
        if failed_results:
            report.append("## Failed Queries")
            report.append("")
            for result in failed_results:
                report.append(f"- {result.query_name}: {result.error_message}")
            report.append("")
        
        return "\n".join(report)