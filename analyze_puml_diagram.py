#!/usr/bin/env python3
"""
Analyze PlantUML Sequence Diagram
==================================
"""

import sys
import os

# Add path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def analyze_puml_file(file_path):
    """Analyze a PlantUML sequence diagram file."""
    
    print("=" * 80)
    print("  PLANTUML SEQUENCE DIAGRAM ANALYSIS")
    print("=" * 80)
    print(f"\nAnalyzing: {file_path}\n")
    
    # Create agent
    agent = SequenceDiagramAgent()
    
    # Analyze the file
    result = agent.analyze_sequence_diagram_file(file_path)
    
    if 'error' in result:
        print(f"ERROR: {result['error']}")
        if 'details' in result:
            print(f"Details: {result['details']}")
        return
    
    # Summary
    print("ANALYSIS SUMMARY")
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
        print("\n\nDETECTED ISSUES:")
        print("=" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. [{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"   Description: {issue.get('description', '')}")
            print(f"   Impact: {issue.get('impact', '')}")
            if issue.get('suggested_fix'):
                print(f"   Suggested Fix: {issue.get('suggested_fix', '')}")
            if issue.get('estimated_improvement'):
                print(f"   Expected Improvement: {issue.get('estimated_improvement', '')}")
            if issue.get('affected_participants'):
                print(f"   Affected Participants: {', '.join(issue.get('affected_participants', []))}")
    
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
    
    # Generate full report
    print("\n\n" + "=" * 80)
    print("FULL REPORT")
    print("=" * 80 + "\n")
    report = agent.generate_report(format='text')
    print(report)
    
    # Also save to file
    output_file = file_path.replace('.puml', '_analysis.txt').replace('.plantuml', '_analysis.txt')
    if not output_file.endswith('_analysis.txt'):
        output_file = file_path + '_analysis.txt'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[INFO] Full report also saved to: {output_file}")
    
    # Generate markdown report
    markdown_file = file_path.replace('.puml', '_analysis.md').replace('.plantuml', '_analysis.md')
    if not markdown_file.endswith('_analysis.md'):
        markdown_file = file_path + '_analysis.md'
    
    markdown_report = agent.generate_report(format='markdown')
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    print(f"[INFO] Markdown report also saved to: {markdown_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_path = "accounts_diagram.puml"
        if os.path.exists(file_path):
            print(f"Using default file: {file_path}\n")
        else:
            print("Usage: python analyze_puml_diagram.py <path_to_diagram.puml>")
            print("\nExample:")
            print("  python analyze_puml_diagram.py accounts_diagram.puml")
            sys.exit(1)
    else:
        file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    
    analyze_puml_file(file_path)

