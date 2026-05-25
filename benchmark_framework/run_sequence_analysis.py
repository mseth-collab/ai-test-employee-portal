#!/usr/bin/env python3
"""
Sequence Diagram Analysis CLI
=============================

Command-line interface for analyzing sequence diagrams and identifying
performance issues.
"""

import argparse
import sys
from pathlib import Path

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def main():
    parser = argparse.ArgumentParser(
        description='Analyze sequence diagrams for performance issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a Mermaid diagram file
  python run_sequence_analysis.py diagram.mmd

  # Analyze a PlantUML diagram file
  python run_sequence_analysis.py diagram.puml --format plantuml

  # Analyze from stdin
  cat diagram.mmd | python run_sequence_analysis.py -

  # Generate markdown report
  python run_sequence_analysis.py diagram.mmd --output report.md --format markdown

  # Show only critical issues
  python run_sequence_analysis.py diagram.mmd --severity critical
        """
    )
    
    parser.add_argument(
        'input',
        help='Input file path or "-" for stdin'
    )
    
    parser.add_argument(
        '--format',
        choices=['auto', 'mermaid', 'plantuml'],
        default='auto',
        help='Diagram format (default: auto-detect)'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--report-format',
        choices=['text', 'markdown', 'json'],
        default='text',
        help='Report format (default: text)'
    )
    
    parser.add_argument(
        '--issue-type',
        help='Filter by issue type (loopy, chatty, projection, paging, etc.)'
    )
    
    parser.add_argument(
        '--severity',
        choices=['low', 'medium', 'high', 'critical'],
        help='Filter by severity level'
    )
    
    parser.add_argument(
        '--list-issues',
        action='store_true',
        help='List all detected issues'
    )
    
    parser.add_argument(
        '--list-corrections',
        action='store_true',
        help='List all corrections'
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input == '-':
        content = sys.stdin.read()
        diagram_format = args.format
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Auto-detect format from extension if not specified
        if args.format == 'auto':
            if input_path.suffix == '.mmd' or 'mermaid' in input_path.name.lower():
                diagram_format = 'mermaid'
            elif input_path.suffix == '.puml' or 'plantuml' in input_path.name.lower():
                diagram_format = 'plantuml'
            else:
                diagram_format = 'auto'
        else:
            diagram_format = args.format
    
    # Analyze
    agent = SequenceDiagramAgent()
    
    try:
        result = agent.analyze_sequence_diagram(content, diagram_format)
        
        if 'error' in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            if 'details' in result:
                print(f"Details: {result['details']}", file=sys.stderr)
            sys.exit(1)
        
        # Handle filtering
        if args.issue_type:
            issues = agent.get_issues_by_type(args.issue_type)
            if not issues:
                print(f"No issues of type '{args.issue_type}' found.")
                sys.exit(0)
            # Create a modified result with filtered issues
            result['analysis']['issues'] = issues
            result['analysis']['total_issues'] = len(issues)
        
        if args.severity:
            issues = agent.get_issues_by_severity(args.severity)
            if not issues:
                print(f"No issues with severity '{args.severity}' found.")
                sys.exit(0)
            result['analysis']['issues'] = issues
            result['analysis']['total_issues'] = len(issues)
        
        # Generate output
        if args.list_issues:
            issues = result.get('analysis', {}).get('issues', [])
            for i, issue in enumerate(issues, 1):
                print(f"{i}. [{issue.get('severity', '').upper()}] {issue.get('type', '')}")
                print(f"   {issue.get('description', '')}")
                print()
        elif args.list_corrections:
            corrections = result.get('corrections', {}).get('corrections', [])
            for i, correction in enumerate(corrections, 1):
                print(f"{i}. {correction.get('description', '')}")
                print(f"   Strategy: {correction.get('strategy', '')}")
                print(f"   Complexity: {correction.get('complexity', '')}")
                print()
        else:
            # Generate full report
            report = agent.generate_report(format=args.report_format)
            
            if args.output:
                output_path = Path(args.output)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"Report written to: {output_path}")
            else:
                print(report)
    
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

