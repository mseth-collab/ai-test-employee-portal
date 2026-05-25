"""
Performance Analysis Module
==========================

This module provides advanced performance analysis capabilities for SQL query benchmarking,
including statistical analysis, anomaly detection, and performance regression detection.
"""

import statistics
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import json
import math


class PerformanceAnalyzer:
    """Analyzes query performance data and provides optimization insights."""
    
    def __init__(self):
        self.analysis_history = []
    
    def analyze_execution_times(self, execution_times: List[float]) -> Dict[str, Any]:
        """
        Comprehensive analysis of execution times.
        
        Args:
            execution_times: List of execution times in milliseconds
            
        Returns:
            Dictionary containing detailed performance analysis
        """
        if not execution_times:
            return {
                "error": "No execution times provided for analysis",
                "analysis_type": "basic_stats"
            }
        
        analysis = {
            "analysis_type": "comprehensive",
            "total_samples": len(execution_times),
            "timestamp": datetime.now().isoformat()
        }
        
        # Basic statistical analysis
        analysis.update(self._analyze_basic_statistics(execution_times))
        
        # Performance trends and patterns
        analysis.update(self._analyze_performance_trends(execution_times))
        
        # Anomaly detection
        analysis.update(self._detect_anomalies(execution_times))
        
        # Performance stability assessment
        analysis.update(self._assess_stability(execution_times))
        
        # Optimization recommendations
        analysis.update(self._generate_optimization_recommendations(execution_times, analysis))
        
        return analysis
    
    def compare_performances(self, baseline_times: List[float], comparison_times: List[float]) -> Dict[str, Any]:
        """
        Compare two sets of performance data to detect regressions or improvements.
        
        Args:
            baseline_times: Baseline execution times
            comparison_times: New execution times for comparison
            
        Returns:
            Dictionary containing comparison analysis
        """
        if not baseline_times or not comparison_times:
            return {"error": "Both baseline and comparison data are required"}
        
        baseline_stats = self._analyze_basic_statistics(baseline_times)
        comparison_stats = self._analyze_basic_statistics(comparison_times)
        
        comparison_analysis = {
            "analysis_type": "performance_comparison",
            "comparison_timestamp": datetime.now().isoformat(),
            "baseline_samples": len(baseline_times),
            "comparison_samples": len(comparison_times)
        }
        
        # Calculate performance differences
        baseline_mean = baseline_stats['mean']
        comparison_mean = comparison_stats['mean']
        mean_difference = comparison_mean - baseline_mean
        percent_change = (mean_difference / baseline_mean) * 100 if baseline_mean > 0 else 0
        
        comparison_analysis.update({
            "baseline_mean_ms": baseline_mean,
            "comparison_mean_ms": comparison_mean,
            "mean_difference_ms": mean_difference,
            "percent_change": percent_change,
            "performance_change": self._classify_performance_change(percent_change)
        })
        
        # Variance comparison
        baseline_std = baseline_stats.get('std_dev', 0)
        comparison_std = comparison_stats.get('std_dev', 0)
        std_change = comparison_std - baseline_std
        
        comparison_analysis.update({
            "baseline_std_dev": baseline_std,
            "comparison_std_dev": comparison_std,
            "std_dev_change": std_change,
            "stability_change": "improved" if std_change < 0 else "degraded" if std_change > 0 else "unchanged"
        })
        
        # Statistical significance test (simplified)
        comparison_analysis.update(self._perform_significance_test(baseline_times, comparison_times))
        
        return comparison_analysis
    
    def analyze_performance_trends(self, execution_times: List[float], timestamps: Optional[List[datetime]] = None) -> Dict[str, Any]:
        """
        Analyze performance trends over time.
        
        Args:
            execution_times: Execution times in chronological order
            timestamps: Optional timestamps for each execution
            
        Returns:
            Dictionary containing trend analysis
        """
        if len(execution_times) < 3:
            return {
                "error": "At least 3 data points required for trend analysis",
                "trend_type": "insufficient_data"
            }
        
        # Use provided timestamps or generate sequential ones
        if timestamps is None:
            timestamps = [datetime.now() - timedelta(minutes=i) for i in range(len(execution_times))]
        
        # Calculate trend using linear regression
        trend_analysis = self._calculate_linear_trend(execution_times, timestamps)
        
        # Identify trend patterns
        trend_patterns = self._identify_trend_patterns(execution_times, timestamps)
        
        return {
            "analysis_type": "trend_analysis",
            "trend_direction": trend_analysis["direction"],
            "trend_slope": trend_analysis["slope"],
            "trend_strength": trend_analysis["strength"],
            "trend_patterns": trend_patterns,
            "forecast": self._forecast_performance(execution_times, timestamps)
        }
    
    def _analyze_basic_statistics(self, execution_times: List[float]) -> Dict[str, Any]:
        """Calculate basic statistical measures."""
        sorted_times = sorted(execution_times)
        
        return {
            "mean": statistics.mean(execution_times),
            "median": statistics.median(execution_times),
            "mode": statistics.mode(execution_times) if len(set(execution_times)) < len(execution_times) else None,
            "std_dev": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            "variance": statistics.variance(execution_times) if len(execution_times) > 1 else 0,
            "min": min(execution_times),
            "max": max(execution_times),
            "range": max(execution_times) - min(execution_times),
            "percentiles": {
                "p25": self._calculate_percentile(execution_times, 25),
                "p75": self._calculate_percentile(execution_times, 75),
                "p90": self._calculate_percentile(execution_times, 90),
                "p95": self._calculate_percentile(execution_times, 95),
                "p99": self._calculate_percentile(execution_times, 99)
            },
            "coefficient_of_variation": (statistics.stdev(execution_times) / statistics.mean(execution_times)) if statistics.mean(execution_times) > 0 else 0
        }
    
    def _analyze_performance_trends(self, execution_times: List[float]) -> Dict[str, Any]:
        """Analyze patterns and trends in performance data."""
        if len(execution_times) < 5:
            return {"trend_type": "insufficient_data"}
        
        # Calculate moving averages
        ma_3 = self._calculate_moving_average(execution_times, 3)
        ma_5 = self._calculate_moving_average(execution_times, 5)
        
        # Detect if performance is improving, degrading, or stable
        recent_times = execution_times[-5:]
        early_times = execution_times[:5]
        
        recent_avg = statistics.mean(recent_times)
        early_avg = statistics.mean(early_times)
        
        change_percent = ((recent_avg - early_avg) / early_avg) * 100 if early_avg > 0 else 0
        
        # Classify trend
        if abs(change_percent) < 5:
            trend_type = "stable"
        elif change_percent > 5:
            trend_type = "degrading"
        else:
            trend_type = "improving"
        
        return {
            "trend_type": trend_type,
            "trend_change_percent": change_percent,
            "moving_average_3": ma_3[-1] if ma_3 else None,
            "moving_average_5": ma_5[-1] if ma_5 else None,
            "performance_direction": "up" if change_percent > 0 else "down",
            "trend_severity": self._classify_trend_severity(abs(change_percent))
        }
    
    def _detect_anomalies(self, execution_times: List[float]) -> Dict[str, Any]:
        """Detect performance anomalies using statistical methods."""
        if len(execution_times) < 10:
            return {"anomaly_detection": "insufficient_data"}
        
        mean_time = statistics.mean(execution_times)
        std_dev = statistics.stdev(execution_times)
        
        # Define anomaly thresholds (2 standard deviations)
        lower_threshold = mean_time - (2 * std_dev)
        upper_threshold = mean_time + (2 * std_dev)
        
        # Identify anomalies
        anomalies = []
        for i, time in enumerate(execution_times):
            if time < lower_threshold or time > upper_threshold:
                anomalies.append({
                    "index": i,
                    "execution_time": time,
                    "deviation_from_mean": time - mean_time,
                    "deviation_std_units": (time - mean_time) / std_dev if std_dev > 0 else 0,
                    "anomaly_type": "fast" if time < lower_threshold else "slow"
                })
        
        # Calculate outlier percentages
        total_samples = len(execution_times)
        outlier_percentage = (len(anomalies) / total_samples) * 100
        
        return {
            "anomaly_detection": "statistical",
            "total_anomalies": len(anomalies),
            "anomaly_percentage": outlier_percentage,
            "anomaly_rate": "high" if outlier_percentage > 10 else "moderate" if outlier_percentage > 5 else "low",
            "lower_threshold": lower_threshold,
            "upper_threshold": upper_threshold,
            "anomalies": anomalies[:5],  # Return first 5 anomalies
            "overall_health": "degraded" if outlier_percentage > 15 else "unstable" if outlier_percentage > 8 else "stable"
        }
    
    def _assess_stability(self, execution_times: List[float]) -> Dict[str, Any]:
        """Assess the stability and consistency of performance."""
        if len(execution_times) < 3:
            return {"stability_assessment": "insufficient_data"}
        
        # Calculate various stability metrics
        cv = statistics.stdev(execution_times) / statistics.mean(execution_times) if statistics.mean(execution_times) > 0 else 0
        
        # Calculate rolling standard deviations
        rolling_std = self._calculate_rolling_std(execution_times, 3)
        
        # Assess stability based on coefficient of variation
        if cv < 0.05:
            stability_level = "very_stable"
        elif cv < 0.1:
            stability_level = "stable"
        elif cv < 0.2:
            stability_level = "moderately_stable"
        elif cv < 0.3:
            stability_level = "unstable"
        else:
            stability_level = "very_unstable"
        
        return {
            "stability_assessment": "comprehensive",
            "coefficient_of_variation": cv,
            "stability_level": stability_level,
            "consistency_score": max(0, 1 - cv),  # Convert to 0-1 scale
            "stability_rating": self._get_stability_rating(cv),
            "rolling_std_avg": statistics.mean(rolling_std) if rolling_std else 0,
            "performance_predictability": "high" if cv < 0.1 else "moderate" if cv < 0.2 else "low"
        }
    
    def _generate_optimization_recommendations(self, execution_times: List[float], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization recommendations based on analysis."""
        recommendations = []
        priority_levels = {"low": 0, "medium": 1, "high": 2}
        
        # Performance-based recommendations
        if "coefficient_of_variation" in analysis and analysis["coefficient_of_variation"] > 0.2:
            recommendations.append({
                "type": "performance_stability",
                "priority": "high",
                "recommendation": "High performance variance detected. Consider implementing query result caching or investigating resource contention.",
                "impact": "Could improve consistency and predictability"
            })
        
        # Anomaly-based recommendations
        anomalies = analysis.get("anomaly_detection", {})
        if anomalies.get("anomaly_rate") in ["high", "moderate"]:
            recommendations.append({
                "type": "anomaly_investigation",
                "priority": "high",
                "recommendation": "Performance anomalies detected. Investigate system resource usage, query execution plans, and external factors.",
                "impact": "Could identify and resolve performance bottlenecks"
            })
        
        # Statistics-based recommendations
        if "mean" in analysis and "max" in analysis:
            mean_time = analysis["mean"]
            max_time = analysis["max"]
            if max_time > (mean_time * 3):
                recommendations.append({
                    "type": "query_optimization",
                    "priority": "medium",
                    "recommendation": "Large gap between average and maximum execution times. Consider optimizing worst-case query paths.",
                    "impact": "Could reduce maximum execution times significantly"
                })
        
        # Trending recommendations
        trends = analysis.get("trend_type", "")
        if trends == "degrading":
            recommendations.append({
                "type": "performance_monitoring",
                "priority": "high",
                "recommendation": "Performance is degrading over time. Investigate data growth, index fragmentation, or system resource changes.",
                "impact": "Could prevent performance degradation"
            })
        
        return {
            "recommendation_count": len(recommendations),
            "recommendations": recommendations,
            "optimization_priority": self._calculate_optimization_priority(recommendations),
            "estimated_improvement": self._estimate_improvement_potential(execution_times, analysis)
        }
    
    def _calculate_linear_trend(self, execution_times: List[float], timestamps: List[datetime]) -> Dict[str, Any]:
        """Calculate linear trend using simple linear regression."""
        if len(execution_times) < 2:
            return {"direction": "unknown", "slope": 0, "strength": 0}
        
        # Convert timestamps to numeric values (days since first timestamp)
        start_time = timestamps[0]
        x_values = [(t - start_time).total_seconds() / 3600 for t in timestamps]  # Hours
        y_values = execution_times
        
        # Calculate linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        # Calculate slope and intercept
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate correlation coefficient (R-squared)
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_values, y_values))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Classify trend direction and strength
        if abs(slope) < 0.01:  # Very small slope
            direction = "stable"
        elif slope > 0:
            direction = "degrading"
        else:
            direction = "improving"
        
        strength = abs(r_squared)
        
        return {
            "direction": direction,
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "strength": "strong" if strength > 0.7 else "moderate" if strength > 0.3 else "weak"
        }
    
    def _identify_trend_patterns(self, execution_times: List[float], timestamps: List[datetime]) -> List[str]:
        """Identify specific patterns in the performance data."""
        patterns = []
        
        if len(execution_times) < 5:
            return patterns
        
        # Check for cyclical patterns
        # Look for repeating patterns every 3-7 data points
        for period in range(3, min(8, len(execution_times) // 2)):
            if self._is_cyclical_pattern(execution_times, period):
                patterns.append(f"cyclical_{period}_period")
        
        # Check for sudden jumps
        for i in range(1, len(execution_times)):
            change_percent = abs((execution_times[i] - execution_times[i-1]) / execution_times[i-1]) * 100
            if change_percent > 50:  # More than 50% change
                patterns.append(f"sudden_jump_at_{i}")
        
        # Check for consistent drift
        first_half = execution_times[:len(execution_times)//2]
        second_half = execution_times[len(execution_times)//2:]
        if first_half and second_half:
            drift = statistics.mean(second_half) - statistics.mean(first_half)
            drift_percent = abs(drift / statistics.mean(first_half)) * 100
            if drift_percent > 20:
                patterns.append(f"consistent_drift_{'up' if drift > 0 else 'down'}")
        
        return patterns
    
    def _forecast_performance(self, execution_times: List[float], timestamps: List[datetime]) -> Dict[str, Any]:
        """Forecast future performance based on current trends."""
        if len(execution_times) < 3:
            return {"forecast": "insufficient_data"}
        
        # Simple linear extrapolation
        recent_times = execution_times[-3:]  # Use last 3 points for trend
        recent_timestamps = timestamps[-3:]
        
        trend_result = self._calculate_linear_trend(recent_times, recent_timestamps)
        slope = trend_result["slope"]
        intercept = trend_result["intercept"]
        
        # Forecast next 5 data points
        last_timestamp = timestamps[-1]
        forecast_points = []
        
        for i in range(1, 6):
            future_time = last_timestamp + timedelta(hours=i)
            x_value = (future_time - timestamps[0]).total_seconds() / 3600
            predicted_time = slope * x_value + intercept
            forecast_points.append({
                "timestamp": future_time.isoformat(),
                "predicted_execution_time": max(0, predicted_time)  # Ensure non-negative
            })
        
        return {
            "forecast_horizon": "5_points",
            "trend_based_forecast": forecast_points,
            "confidence": trend_result["strength"],
            "forecast_direction": trend_result["direction"]
        }
    
    def _perform_significance_test(self, baseline: List[float], comparison: List[float]) -> Dict[str, Any]:
        """Perform simplified statistical significance test."""
        # Using basic t-test approximation
        baseline_mean = statistics.mean(baseline)
        comparison_mean = statistics.mean(comparison)
        
        # Calculate pooled standard deviation
        n1, n2 = len(baseline), len(comparison)
        s1 = statistics.stdev(baseline) if n1 > 1 else 0
        s2 = statistics.stdev(comparison) if n2 > 1 else 0
        
        pooled_std = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
        
        # Calculate t-statistic
        if pooled_std > 0 and n1 + n2 > 2:
            t_statistic = abs(comparison_mean - baseline_mean) / (pooled_std * math.sqrt(1/n1 + 1/n2))
            # Simplified significance assessment
            is_significant = t_statistic > 2.0  # Approximate 95% confidence
        else:
            t_statistic = 0
            is_significant = False
        
        return {
            "significance_test": "t_test_approximation",
            "t_statistic": t_statistic,
            "is_significantly_different": is_significant,
            "confidence_level": "95%" if is_significant else "not_significant"
        }
    
    def _calculate_moving_average(self, data: List[float], window: int) -> List[float]:
        """Calculate moving average for given window size."""
        if len(data) < window:
            return []
        
        result = []
        for i in range(window - 1, len(data)):
            window_data = data[i - window + 1:i + 1]
            result.append(statistics.mean(window_data))
        
        return result
    
    def _calculate_rolling_std(self, data: List[float], window: int) -> List[float]:
        """Calculate rolling standard deviation."""
        if len(data) < window or window < 2:
            return []
        
        result = []
        for i in range(window - 1, len(data)):
            window_data = data[i - window + 1:i + 1]
            result.append(statistics.stdev(window_data))
        
        return result
    
    def _is_cyclical_pattern(self, data: List[float], period: int) -> bool:
        """Check if data has cyclical pattern with given period."""
        if len(data) < period * 2:
            return False
        
        # Check correlation between pattern segments
        correlations = []
        for i in range(period, len(data) - period):
            segment1 = data[i-period:i]
            segment2 = data[i:i+period]
            if len(segment1) == len(segment2) == period:
                # Simple correlation calculation
                correlation = self._calculate_correlation(segment1, segment2)
                if correlation > 0.7:  # Strong correlation threshold
                    correlations.append(correlation)
        
        return len(correlations) > len(data) / period * 0.5  # At least 50% of possible correlations
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient between two lists."""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi**2 for xi in x)
        sum_y2 = sum(yi**2 for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
        
        return numerator / denominator if denominator != 0 else 0
    
    def _classify_performance_change(self, percent_change: float) -> str:
        """Classify performance change based on percentage."""
        if abs(percent_change) < 2:
            return "negligible"
        elif abs(percent_change) < 10:
            return "minor"
        elif abs(percent_change) < 25:
            return "moderate"
        else:
            return "significant"
    
    def _classify_trend_severity(self, change_percent: float) -> str:
        """Classify trend severity based on percentage change."""
        if change_percent < 5:
            return "negligible"
        elif change_percent < 15:
            return "moderate"
        elif change_percent < 30:
            return "significant"
        else:
            return "severe"
    
    def _get_stability_rating(self, cv: float) -> str:
        """Get stability rating based on coefficient of variation."""
        if cv < 0.05:
            return "excellent"
        elif cv < 0.1:
            return "good"
        elif cv < 0.2:
            return "fair"
        elif cv < 0.3:
            return "poor"
        else:
            return "very_poor"
    
    def _calculate_optimization_priority(self, recommendations: List[Dict[str, Any]]) -> str:
        """Calculate overall optimization priority."""
        if not recommendations:
            return "low"
        
        priority_weights = {"low": 1, "medium": 2, "high": 3}
        total_priority = sum(priority_weights.get(rec.get("priority", "low"), 1) for rec in recommendations)
        avg_priority = total_priority / len(recommendations)
        
        if avg_priority >= 2.5:
            return "high"
        elif avg_priority >= 1.5:
            return "medium"
        else:
            return "low"
    
    def _estimate_improvement_potential(self, execution_times: List[float], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate potential for performance improvement."""
        current_mean = analysis.get("mean", 0)
        outliers = analysis.get("anomaly_detection", {}).get("total_anomalies", 0)
        total_samples = analysis.get("total_samples", 1)
        
        # Estimate improvement potential based on outliers and stability
        outlier_rate = (outliers / total_samples) * 100 if total_samples > 0 else 0
        cv = analysis.get("coefficient_of_variation", 0)
        
        potential_improvement = min(30, outlier_rate * 2 + cv * 50)  # Cap at 30%
        
        return {
            "estimated_improvement_percent": potential_improvement,
            "improvement_potential": "high" if potential_improvement > 20 else "moderate" if potential_improvement > 10 else "low",
            "focus_areas": ["performance_stability"] if cv > 0.2 else ["anomaly_elimination"] if outlier_rate > 10 else ["general_optimization"]
        }
    
    def _calculate_percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile for a given data set."""
        if not data:
            return 0
        
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight