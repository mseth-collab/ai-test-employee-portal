#!/usr/bin/env python3
"""
Comprehensive Demo - Shows Multiple Issue Types
================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def demo_multiple_issues():
    """Demo with multiple performance issues."""
    print("\n" + "=" * 80)
    print("  COMPREHENSIVE DEMO - Multiple Performance Issues")
    print("=" * 80 + "\n")
    
    # Diagram with multiple issues: loopy, chatty, projection
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Note over Client,Database: Scenario with multiple performance issues
    
    Client->>API: getProduct(1)
    API->>Database: SELECT * FROM products WHERE id = 1
    Database-->>API: product1
    API-->>Client: product1
    
    Client->>API: getProduct(2)
    API->>Database: SELECT * FROM products WHERE id = 2
    Database-->>API: product2
    API-->>Client: product2
    
    Client->>API: getProduct(3)
    API->>Database: SELECT * FROM products WHERE id = 3
    Database-->>API: product3
    API-->>Client: product3
    
    Client->>API: getProduct(4)
    API->>Database: SELECT * FROM products WHERE id = 4
    Database-->>API: product4
    API-->>Client: product4
    
    Client->>API: getProduct(5)
    API->>Database: SELECT * FROM products WHERE id = 5
    Database-->>API: product5
    API-->>Client: product5
    
    Client->>API: getAllUsers()
    API->>Database: SELECT * FROM users
    Database-->>API: allUsers[10000 items]
    API->>API: filter(users, active=true)
    API-->>Client: activeUsers[500 items]
    
    Client->>API: getPage(1)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 0
    Database-->>API: page1
    API-->>Client: page1
    
    Client->>API: getPage(2)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 10
    Database-->>API: page2
    API-->>Client: page2
"""
    
    print("INPUT DIAGRAM:")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    print("ANALYZING...")
    print("-" * 80 + "\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    # Summary
    print("ANALYSIS SUMMARY:")
    print("-" * 80)
    print(f"Total Messages Parsed: {result.get('parsed_data', {}).get('total_messages', 0)}")
    print(f"Total Participants: {result.get('parsed_data', {}).get('total_participants', 0)}")
    print(f"Total Issues Detected: {result.get('analysis', {}).get('total_issues', 0)}")
    print(f"Overall Risk Level: {result.get('analysis', {}).get('risk_level', 'unknown').upper()}")
    
    # Issues breakdown
    summary = result.get('analysis', {}).get('summary', {})
    issue_breakdown = summary.get('issue_breakdown', {})
    if issue_breakdown:
        print("\nISSUES BY TYPE:")
        print("-" * 80)
        for issue_type, count in issue_breakdown.items():
            print(f"  {issue_type.upper()}: {count}")
    
    # Show all issues
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("\n\nDETECTED ISSUES (Detailed):")
        print("=" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. [{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"   Description: {issue.get('description', '')}")
            print(f"   Impact: {issue.get('impact', '')}")
            if issue.get('suggested_fix'):
                print(f"   Suggested Fix: {issue.get('suggested_fix', '')}")
            if issue.get('estimated_improvement'):
                print(f"   Expected Improvement: {issue.get('estimated_improvement', '')}")
    
    # Show corrections
    corrections = result.get('corrections', {}).get('corrections', [])
    if corrections:
        print("\n\n" + "=" * 80)
        print("GENERATED CORRECTIONS:")
        print("=" * 80)
        for i, correction in enumerate(corrections, 1):
            print(f"\n{i}. {correction.get('description', '')}")
            print(f"   Strategy: {correction.get('strategy', '').upper()}")
            print(f"   Complexity: {correction.get('complexity', '').upper()}")
            if correction.get('expected_improvement'):
                print(f"   Expected Improvement: {correction.get('expected_improvement', '')}")
            
            if correction.get('code_example'):
                print(f"\n   Code Example:")
                print("   " + "-" * 76)
                code_lines = correction.get('code_example', '').strip().split('\n')
                for line in code_lines:
                    if line.strip():
                        print(f"   {line}")
                print("   " + "-" * 76)
            
            if correction.get('implementation_steps'):
                print(f"\n   Implementation Steps:")
                for step in correction.get('implementation_steps', []):
                    print(f"     {step}")
    
    # Show report preview
    print("\n\n" + "=" * 80)
    print("FULL REPORT (Text Format):")
    print("=" * 80 + "\n")
    report = agent.generate_report(format='text')
    print(report)
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    demo_multiple_issues()

