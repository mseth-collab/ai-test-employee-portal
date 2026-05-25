#!/usr/bin/env python3
"""
Quick Demo - Sequence Diagram Analysis Agent
============================================

A quick demonstration showing the agent in action.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def main():
    """Run quick demo."""
    print_header("SEQUENCE DIAGRAM ANALYSIS AGENT - QUICK DEMO")
    
    # Example: Classic N+1 problem
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: getOrders()
    API->>Database: SELECT * FROM orders WHERE user_id = 123
    Database-->>API: orders[10 items]
    API-->>Client: orders[10 items]
    
    loop For each order
        Client->>API: getOrderDetails(orderId)
        API->>Database: SELECT * FROM order_items WHERE order_id = ?
        Database-->>API: items[]
        API-->>Client: items[]
    end
"""
    
    print("INPUT: Sequence Diagram with N+1 Problem")
    print("-" * 80)
    print(diagram)
    
    print("\n" + "=" * 80)
    print("  ANALYZING...")
    print("=" * 80 + "\n")
    
    # Analyze
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    # Show results
    print("RESULTS:")
    print("-" * 80)
    print(f"[OK] Parsed {result.get('parsed_data', {}).get('total_messages', 0)} messages")
    print(f"[OK] Detected {result.get('analysis', {}).get('total_issues', 0)} performance issues")
    print(f"[OK] Risk Level: {result.get('analysis', {}).get('risk_level', 'unknown').upper()}")
    print(f"[OK] Generated {result.get('corrections', {}).get('total_corrections', 0)} corrections")
    
    # Show issues
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("\n\nDETECTED ISSUES:")
        print("-" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. [{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"   {issue.get('description', '')}")
            print(f"   Impact: {issue.get('impact', '')}")
    
    # Show corrections
    corrections = result.get('corrections', {}).get('corrections', [])
    if corrections:
        print("\n\nGENERATED CORRECTIONS:")
        print("-" * 80)
        for i, correction in enumerate(corrections, 1):
            print(f"\n{i}. {correction.get('description', '')}")
            print(f"   Strategy: {correction.get('strategy', '').upper()}")
            if correction.get('code_example'):
                print(f"\n   Code Example:")
                print("   " + "-" * 76)
                for line in correction.get('code_example', '').split('\n'):
                    if line.strip():
                        print(f"   {line}")
                print("   " + "-" * 76)
            if correction.get('expected_improvement'):
                print(f"\n   Expected: {correction.get('expected_improvement', '')}")
    
    # Show summary report
    print("\n\n" + "=" * 80)
    print("  SUMMARY REPORT")
    print("=" * 80 + "\n")
    report = agent.generate_report(format='text')
    print(report)
    
    print("\n" + "=" * 80)
    print("  DEMO COMPLETE!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

