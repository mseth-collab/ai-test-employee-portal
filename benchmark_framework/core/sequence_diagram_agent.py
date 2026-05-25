"""
Sequence Diagram Analysis Agent
================================

Main orchestrator agent that parses sequence diagrams, identifies performance issues,
and generates corrections.
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
import json

from .seqparser import parse_mermaid_sequence, parse_plantuml_sequence
from .sequence_diagram_analyzer import SequenceDiagramAnalyzer
from .correction_agent import CorrectionAgent


class SequenceDiagramAgent:
    """
    Main agent for analyzing sequence diagrams and identifying performance issues.
    
    This agent:
    1. Parses sequence diagrams (Mermaid or PlantUML)
    2. Analyzes for performance issues (loopy, chatty, projections, paging, etc.)
    3. Generates corrections and suggestions
    """
    
    def __init__(self):
        self.analyzer = SequenceDiagramAnalyzer()
        self.correction_agent = CorrectionAgent()
        self.parsed_data: Optional[Dict] = None
        self.analysis_result: Optional[Dict] = None
        self.corrections: Optional[Dict] = None
    
    def analyze_sequence_diagram(
        self, 
        diagram_content: str, 
        diagram_format: str = "auto"
    ) -> Dict:
        """
        Analyze a sequence diagram for performance issues.
        
        Args:
            diagram_content: Content of the sequence diagram
            diagram_format: Format of diagram ("mermaid", "plantuml", or "auto" for auto-detect)
            
        Returns:
            Dictionary containing analysis results and corrections
        """
        # Parse the diagram
        parsed_data = self._parse_diagram(diagram_content, diagram_format)
        if not parsed_data or 'error' in parsed_data:
            return {
                'error': 'Failed to parse sequence diagram',
                'details': parsed_data.get('error', 'Unknown error')
            }
        
        self.parsed_data = parsed_data
        
        # Analyze for issues
        analysis_result = self.analyzer.analyze(parsed_data)
        self.analysis_result = analysis_result
        
        # Generate corrections
        corrections = self.correction_agent.generate_corrections(analysis_result, parsed_data)
        self.corrections = corrections
        
        # Combine results
        return {
            'parsed_data': {
                'total_messages': parsed_data.get('total_messages', 0),
                'total_participants': parsed_data.get('total_participants', 0),
                'participants': parsed_data.get('participants', [])
            },
            'analysis': analysis_result,
            'corrections': corrections,
            'summary': self._generate_overall_summary()
        }
    
    def analyze_sequence_diagram_file(
        self, 
        file_path: Union[str, Path]
    ) -> Dict:
        """
        Analyze a sequence diagram from a file.
        
        Args:
            file_path: Path to the sequence diagram file
            
        Returns:
            Dictionary containing analysis results and corrections
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Auto-detect format from file extension
            file_path_obj = Path(file_path)
            if file_path_obj.suffix == '.mmd' or 'mermaid' in file_path_obj.name.lower():
                format_type = 'mermaid'
            elif file_path_obj.suffix == '.puml' or 'plantuml' in file_path_obj.name.lower():
                format_type = 'plantuml'
            else:
                format_type = 'auto'
            
            return self.analyze_sequence_diagram(content, format_type)
        except Exception as e:
            return {
                'error': f'Failed to read file: {str(e)}'
            }
    
    def get_issues_by_type(self, issue_type: str) -> List[Dict]:
        """
        Get all issues of a specific type.
        
        Args:
            issue_type: Type of issue (loopy, chatty, projection, paging, etc.)
            
        Returns:
            List of issues matching the type
        """
        if not self.analysis_result:
            return []
        
        issues = self.analysis_result.get('issues', [])
        return [issue for issue in issues if issue.get('type') == issue_type]
    
    def get_issues_by_severity(self, severity: str) -> List[Dict]:
        """
        Get all issues of a specific severity.
        
        Args:
            severity: Severity level (low, medium, high, critical)
            
        Returns:
            List of issues matching the severity
        """
        if not self.analysis_result:
            return []
        
        issues = self.analysis_result.get('issues', [])
        return [issue for issue in issues if issue.get('severity') == severity]
    
    def get_corrections_for_issue_type(self, issue_type: str) -> List[Dict]:
        """
        Get corrections for a specific issue type.
        
        Args:
            issue_type: Type of issue
            
        Returns:
            List of corrections for that issue type
        """
        if not self.corrections:
            return []
        
        corrections = self.corrections.get('corrections', [])
        return [corr for corr in corrections if corr.get('issue_type') == issue_type]
    
    def generate_report(self, format: str = 'text') -> str:
        """
        Generate a human-readable report.
        
        Args:
            format: Report format ('text', 'json', 'markdown')
            
        Returns:
            Formatted report string
        """
        if not self.analysis_result:
            return "No analysis available. Please run analyze_sequence_diagram() first."
        
        if format == 'json':
            return json.dumps({
                'analysis': self.analysis_result,
                'corrections': self.corrections
            }, indent=2)
        
        if format == 'markdown':
            return self._generate_markdown_report()
        
        return self._generate_text_report()
    
    def _parse_diagram(self, content: str, format: str) -> Optional[Dict]:
        """Parse diagram based on format."""
        if format == 'auto':
            # Auto-detect format
            if 'sequenceDiagram' in content or 'mermaid' in content.lower():
                format = 'mermaid'
            elif '@startuml' in content or 'plantuml' in content.lower():
                format = 'plantuml'
            else:
                # Try mermaid first
                try:
                    result = parse_mermaid_sequence(content)
                    if result.get('messages'):
                        return result
                except:
                    pass
                # Try plantuml
                try:
                    result = parse_plantuml_sequence(content)
                    if result.get('messages'):
                        return result
                except:
                    pass
                return {'error': 'Could not auto-detect diagram format'}
        
        if format == 'mermaid':
            return parse_mermaid_sequence(content)
        elif format == 'plantuml':
            return parse_plantuml_sequence(content)
        else:
            return {'error': f'Unsupported format: {format}'}
    
    def _generate_overall_summary(self) -> Dict:
        """Generate overall summary of analysis."""
        if not self.analysis_result:
            return {}
        
        analysis_summary = self.analysis_result.get('summary', {})
        corrections_summary = self.corrections.get('summary', {}) if self.corrections else {}
        
        return {
            'total_issues': self.analysis_result.get('total_issues', 0),
            'risk_level': self.analysis_result.get('risk_level', 'unknown'),
            'issue_breakdown': analysis_summary.get('issue_breakdown', {}),
            'total_corrections': corrections_summary.get('total_corrections', 0),
            'recommended_actions': analysis_summary.get('recommended_actions', 0)
        }
    
    def _generate_text_report(self) -> str:
        """Generate plain text report."""
        if not self.analysis_result:
            return "No analysis available."
        
        report = []
        report.append("=" * 80)
        report.append("SEQUENCE DIAGRAM PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        summary = self._generate_overall_summary()
        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Issues Detected: {summary.get('total_issues', 0)}")
        report.append(f"Risk Level: {summary.get('risk_level', 'unknown').upper()}")
        report.append(f"Total Corrections Available: {summary.get('total_corrections', 0)}")
        report.append("")
        
        # Issues by type
        issue_breakdown = summary.get('issue_breakdown', {})
        if issue_breakdown:
            report.append("ISSUES BY TYPE")
            report.append("-" * 80)
            for issue_type, count in issue_breakdown.items():
                report.append(f"  {issue_type.upper()}: {count}")
            report.append("")
        
        # Critical and High Priority Issues
        critical_issues = self.get_issues_by_severity('critical')
        high_issues = self.get_issues_by_severity('high')
        
        if critical_issues or high_issues:
            report.append("CRITICAL & HIGH PRIORITY ISSUES")
            report.append("-" * 80)
            
            for issue in critical_issues + high_issues:
                report.append(f"\n[{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
                report.append(f"  Description: {issue.get('description', '')}")
                report.append(f"  Impact: {issue.get('impact', '')}")
                if issue.get('suggested_fix'):
                    report.append(f"  Suggested Fix: {issue.get('suggested_fix', '')}")
                report.append("")
        
        # Corrections
        if self.corrections:
            corrections = self.corrections.get('corrections', [])
            if corrections:
                report.append("CORRECTIONS & RECOMMENDATIONS")
                report.append("-" * 80)
                
                for i, correction in enumerate(corrections, 1):
                    report.append(f"\n{i}. {correction.get('description', '')}")
                    report.append(f"   Strategy: {correction.get('strategy', '').upper()}")
                    report.append(f"   Complexity: {correction.get('complexity', '').upper()}")
                    if correction.get('expected_improvement'):
                        report.append(f"   Expected Improvement: {correction.get('expected_improvement', '')}")
                    report.append("")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown report."""
        if not self.analysis_result:
            return "# No Analysis Available"
        
        report = []
        report.append("# Sequence Diagram Performance Analysis Report")
        report.append("")
        
        # Summary
        summary = self._generate_overall_summary()
        report.append("## Summary")
        report.append("")
        report.append(f"- **Total Issues**: {summary.get('total_issues', 0)}")
        report.append(f"- **Risk Level**: {summary.get('risk_level', 'unknown').upper()}")
        report.append(f"- **Total Corrections**: {summary.get('total_corrections', 0)}")
        report.append("")
        
        # Issues
        issues = self.analysis_result.get('issues', [])
        if issues:
            report.append("## Detected Issues")
            report.append("")
            
            for issue in issues:
                severity_emoji = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(issue.get('severity', ''), '⚪')
                
                report.append(f"### {severity_emoji} {issue.get('type', '').upper()} - {issue.get('severity', '').upper()}")
                report.append("")
                report.append(f"**Description**: {issue.get('description', '')}")
                report.append("")
                report.append(f"**Impact**: {issue.get('impact', '')}")
                report.append("")
                if issue.get('suggested_fix'):
                    report.append(f"**Suggested Fix**: {issue.get('suggested_fix', '')}")
                    report.append("")
        
        # Corrections
        if self.corrections:
            corrections = self.corrections.get('corrections', [])
            if corrections:
                report.append("## Corrections & Recommendations")
                report.append("")
                
                for i, correction in enumerate(corrections, 1):
                    report.append(f"### {i}. {correction.get('description', '')}")
                    report.append("")
                    report.append(f"- **Strategy**: {correction.get('strategy', '')}")
                    report.append(f"- **Complexity**: {correction.get('complexity', '')}")
                    report.append(f"- **Expected Improvement**: {correction.get('expected_improvement', '')}")
                    report.append("")
                    
                    if correction.get('code_example'):
                        report.append("**Code Example:**")
                        report.append("")
                        report.append("```python")
                        report.append(correction.get('code_example', '').strip())
                        report.append("```")
                        report.append("")
                    
                    if correction.get('implementation_steps'):
                        report.append("**Implementation Steps:**")
                        report.append("")
                        for step in correction.get('implementation_steps', []):
                            report.append(f"- {step}")
                        report.append("")
        
        return "\n".join(report)

