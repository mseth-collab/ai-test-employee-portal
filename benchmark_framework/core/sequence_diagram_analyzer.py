"""
Sequence Diagram Performance Analyzer
====================================

This module provides comprehensive analysis of sequence diagrams to identify
performance issues including loopy patterns, chatty interfaces, projection issues,
paging problems, and other performance degradation patterns.
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class IssueType(Enum):
    """Types of performance issues that can be detected."""
    LOOPY = "loopy"
    CHATTY = "chatty"
    PROJECTION = "projection"
    PAGING = "paging"
    BOTTLENECK = "bottleneck"
    LONG_CHAIN = "long_chain"
    ROUND_TRIP = "round_trip"
    MISSING_PARALLELIZATION = "missing_parallelization"


class Severity(Enum):
    """Severity levels for detected issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PerformanceIssue:
    """Represents a detected performance issue."""
    issue_type: IssueType
    severity: Severity
    description: str
    location: Dict[str, any]  # Messages, participants, or patterns involved
    impact: str
    affected_participants: List[str] = field(default_factory=list)
    message_indices: List[int] = field(default_factory=list)
    suggested_fix: Optional[str] = None
    estimated_improvement: Optional[str] = None


class SequenceDiagramAnalyzer:
    """
    Analyzes sequence diagrams to identify performance issues.
    
    Detects:
    - Loopy: Repeated patterns that could be optimized
    - Chatty: Too many small calls (N+1 problem)
    - Projections: Inefficient data fetching patterns
    - Paging: Pagination issues
    - Other performance degradation patterns
    """
    
    def __init__(self):
        self.issues: List[PerformanceIssue] = []
        self.parsed_data: Optional[Dict] = None
        
    def analyze(self, parsed_data: Dict) -> Dict:
        """
        Perform comprehensive analysis of a parsed sequence diagram.
        
        Args:
            parsed_data: Parsed sequence diagram data from seqparser
            
        Returns:
            Dictionary containing all detected issues and analysis results
        """
        self.parsed_data = parsed_data
        self.issues = []
        
        messages = parsed_data.get('messages', [])
        participants = parsed_data.get('participants', [])
        
        if not messages:
            return {
                'error': 'No messages found in sequence diagram',
                'issues': [],
                'summary': {}
            }
        
        # Detect all types of issues
        self._detect_loopy_patterns(messages, participants)
        self._detect_chatty_patterns(messages, participants)
        self._detect_projection_issues(messages, participants)
        self._detect_paging_issues(messages, participants)
        self._detect_bottlenecks(messages, participants)
        self._detect_long_chains(messages, participants)
        self._detect_round_trip_patterns(messages, participants)
        self._detect_missing_parallelization(messages, participants)
        
        # Generate summary
        summary = self._generate_summary()
        
        return {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_messages': len(messages),
            'total_participants': len(participants),
            'total_issues': len(self.issues),
            'issues': [self._issue_to_dict(issue) for issue in self.issues],
            'summary': summary,
            'risk_level': self._calculate_overall_risk()
        }
    
    def _detect_loopy_patterns(self, messages: List[Dict], participants: List[str]):
        """
        Detect loopy patterns - repeated sequences that could be optimized.
        
        Loopy patterns include:
        - Repeated calls to the same participant with similar messages
        - Loops in sequence (A->B->A->B)
        - Iterative patterns that could be batched
        """
        # Look for repeated patterns (same from->to with similar messages)
        pattern_counts = defaultdict(int)
        pattern_locations = defaultdict(list)
        
        for i, msg in enumerate(messages):
            # Create a pattern key based on from, to, and message similarity
            pattern_key = f"{msg['from']}->{msg['to']}"
            message_words = set(re.findall(r'\w+', msg['message'].lower()))
            
            # Check if this pattern repeats
            for j, other_msg in enumerate(messages):
                if i != j:
                    other_pattern = f"{other_msg['from']}->{other_msg['to']}"
                    other_words = set(re.findall(r'\w+', other_msg['message'].lower()))
                    
                    # If same pattern and similar message (at least 50% word overlap)
                    if pattern_key == other_pattern:
                        overlap = len(message_words & other_words) / max(len(message_words | other_words), 1)
                        if overlap > 0.5:
                            pattern_key_full = f"{pattern_key}:{sorted(message_words)}"
                            pattern_counts[pattern_key_full] += 1
                            if i not in pattern_locations[pattern_key_full]:
                                pattern_locations[pattern_key_full].append(i)
                            if j not in pattern_locations[pattern_key_full]:
                                pattern_locations[pattern_key_full].append(j)
        
        # Identify loopy patterns (3+ repetitions)
        for pattern, count in pattern_counts.items():
            if count >= 3:
                locations = sorted(pattern_locations[pattern])
                severity = Severity.CRITICAL if count >= 10 else Severity.HIGH if count >= 5 else Severity.MEDIUM
                
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.LOOPY,
                    severity=severity,
                    description=f"Loopy pattern detected: {pattern.split(':')[0]} repeated {count} times",
                    location={'pattern': pattern, 'repetitions': count},
                    impact=f"Performance degradation due to {count} repeated calls. Consider batching or caching.",
                    affected_participants=[pattern.split('->')[0], pattern.split('->')[1].split(':')[0]],
                    message_indices=locations,
                    suggested_fix="Batch multiple calls into a single request or implement caching",
                    estimated_improvement=f"Potential {min(50, count * 5)}% improvement by batching"
                ))
        
        # Detect circular patterns (A->B->A->B)
        for i in range(len(messages) - 3):
            msg1, msg2, msg3, msg4 = messages[i], messages[i+1], messages[i+2], messages[i+3] if i+3 < len(messages) else None
            
            if msg4 and msg1['from'] == msg3['from'] == msg1['to'] and \
               msg2['from'] == msg4['from'] == msg2['to']:
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.LOOPY,
                    severity=Severity.HIGH,
                    description="Circular call pattern detected (ping-pong pattern)",
                    location={'pattern': 'circular', 'messages': [i, i+1, i+2, i+3]},
                    impact="Round-trip overhead causing performance degradation",
                    affected_participants=[msg1['from'], msg1['to']],
                    message_indices=[i, i+1, i+2, i+3],
                    suggested_fix="Combine operations or use async/batch processing",
                    estimated_improvement="30-50% improvement by reducing round-trips"
                ))
    
    def _detect_chatty_patterns(self, messages: List[Dict], participants: List[str]):
        """
        Detect chatty patterns - too many small calls (N+1 problem).
        
        Chatty patterns include:
        - Many small calls to the same participant
        - N+1 query patterns (one call followed by N calls)
        - Excessive back-and-forth communication
        """
        # Count calls per participant
        participant_call_counts = defaultdict(int)
        participant_call_locations = defaultdict(list)
        
        for i, msg in enumerate(messages):
            participant_call_counts[msg['to']] += 1
            participant_call_locations[msg['to']].append(i)
        
        # Identify chatty participants (receiving many calls)
        for participant, count in participant_call_counts.items():
            if count >= 5:  # Threshold for chatty
                severity = Severity.CRITICAL if count >= 20 else Severity.HIGH if count >= 10 else Severity.MEDIUM
                
                # Check if calls are from multiple sources (N+1 pattern)
                callers = set(messages[i]['from'] for i in participant_call_locations[participant])
                is_n_plus_one = len(callers) > 1 and count >= 5
                
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.CHATTY,
                    severity=severity,
                    description=f"Chatty interface: {participant} receives {count} calls",
                    location={'participant': participant, 'call_count': count, 'callers': list(callers)},
                    impact=f"Performance degradation due to {count} individual calls. Consider batching.",
                    affected_participants=[participant] + list(callers),
                    message_indices=participant_call_locations[participant],
                    suggested_fix="Batch multiple calls into a single request or use bulk operations",
                    estimated_improvement=f"Potential {min(70, count * 3)}% improvement by batching"
                ))
        
        # Detect N+1 patterns specifically
        # Look for: one call followed by many calls to the same participant
        for i in range(len(messages) - 1):
            msg1 = messages[i]
            # Count subsequent calls to the same participant
            subsequent_calls = []
            for j in range(i + 1, min(i + 20, len(messages))):  # Look ahead up to 20 messages
                if messages[j]['to'] == msg1['to'] and messages[j]['from'] == msg1['from']:
                    subsequent_calls.append(j)
            
            if len(subsequent_calls) >= 3:  # N+1 pattern threshold
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.CHATTY,
                    severity=Severity.HIGH,
                    description=f"N+1 pattern detected: {msg1['from']} makes {len(subsequent_calls) + 1} calls to {msg1['to']}",
                    location={'pattern': 'n_plus_one', 'initial_call': i, 'subsequent_calls': subsequent_calls},
                    impact="Classic N+1 problem causing excessive network/database calls",
                    affected_participants=[msg1['from'], msg1['to']],
                    message_indices=[i] + subsequent_calls,
                    suggested_fix="Use eager loading, batch queries, or join operations to fetch all data in one call",
                    estimated_improvement="60-80% improvement by eliminating N+1 pattern"
                ))
    
    def _detect_projection_issues(self, messages: List[Dict], participants: List[str]):
        """
        Detect projection issues - inefficient data fetching patterns.
        
        Projection issues include:
        - Fetching all data then filtering (SELECT * patterns)
        - Multiple calls to fetch related data that could be joined
        - Over-fetching data
        """
        # Look for messages that suggest data fetching
        fetch_keywords = ['get', 'fetch', 'load', 'query', 'select', 'find', 'retrieve', 'read']
        projection_keywords = ['all', 'list', 'items', 'data', 'records', 'rows']
        
        projection_issues = []
        
        for i, msg in enumerate(messages):
            message_lower = msg['message'].lower()
            
            # Check for over-fetching patterns
            has_fetch = any(keyword in message_lower for keyword in fetch_keywords)
            has_projection = any(keyword in message_lower for keyword in projection_keywords)
            
            if has_fetch and has_projection:
                # Check if there are subsequent filter/process calls
                has_subsequent_filter = False
                for j in range(i + 1, min(i + 5, len(messages))):
                    filter_keywords = ['filter', 'where', 'process', 'transform', 'map']
                    if any(kw in messages[j]['message'].lower() for kw in filter_keywords):
                        has_subsequent_filter = True
                        break
                
                if has_subsequent_filter:
                    projection_issues.append({
                        'index': i,
                        'message': msg,
                        'issue': 'fetch_all_then_filter'
                    })
        
        # Group related projection issues
        if projection_issues:
            self.issues.append(PerformanceIssue(
                issue_type=IssueType.PROJECTION,
                severity=Severity.MEDIUM,
                description=f"Projection issue: Fetching all data then filtering ({len(projection_issues)} occurrences)",
                location={'issues': projection_issues},
                impact="Inefficient data fetching - fetching more data than needed",
                affected_participants=list(set(msg['to'] for issue in projection_issues for msg in [issue['message']])),
                message_indices=[issue['index'] for issue in projection_issues],
                suggested_fix="Push filters to the data source (database/API) to fetch only needed data",
                estimated_improvement="40-60% improvement by filtering at source"
            ))
        
        # Detect multiple calls that could be a single join
        # Look for: get A, then get B related to A
        for i in range(len(messages) - 1):
            msg1 = messages[i]
            msg2 = messages[i + 1]
            
            if msg1['from'] == msg2['from'] and msg1['to'] != msg2['to']:
                msg1_lower = msg1['message'].lower()
                msg2_lower = msg2['message'].lower()
                
                if any(kw in msg1_lower for kw in fetch_keywords) and \
                   any(kw in msg2_lower for kw in fetch_keywords):
                    # Potential join opportunity
                    relation_keywords = ['by', 'for', 'with', 'related', 'associated']
                    if any(kw in msg2_lower for kw in relation_keywords):
                        self.issues.append(PerformanceIssue(
                            issue_type=IssueType.PROJECTION,
                            severity=Severity.MEDIUM,
                            description="Projection issue: Multiple separate calls that could be a join",
                            location={'calls': [i, i+1]},
                            impact="Multiple round-trips instead of a single joined query",
                            affected_participants=[msg1['from'], msg1['to'], msg2['to']],
                            message_indices=[i, i+1],
                            suggested_fix="Use a single query with JOIN or batch operation to fetch related data",
                            estimated_improvement="50-70% improvement by using joins"
                        ))
    
    def _detect_paging_issues(self, messages: List[Dict], participants: List[str]):
        """
        Detect paging issues - inefficient pagination patterns.
        
        Paging issues include:
        - Fetching pages sequentially when parallel is possible
        - Small page sizes causing many calls
        - No pagination when large datasets are fetched
        """
        paging_keywords = ['page', 'pagination', 'offset', 'limit', 'skip', 'take', 'next', 'prev']
        
        paging_calls = []
        for i, msg in enumerate(messages):
            message_lower = msg['message'].lower()
            if any(kw in message_lower for kw in paging_keywords):
                paging_calls.append(i)
        
        # Detect sequential paging (many page requests)
        if len(paging_calls) >= 3:
            # Check if they're sequential
            is_sequential = all(paging_calls[j+1] - paging_calls[j] <= 3 for j in range(len(paging_calls) - 1))
            
            if is_sequential:
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.PAGING,
                    severity=Severity.MEDIUM,
                    description=f"Paging issue: {len(paging_calls)} sequential page requests detected",
                    location={'paging_calls': paging_calls},
                    impact="Sequential pagination causing performance degradation",
                    affected_participants=list(set(messages[i]['to'] for i in paging_calls)),
                    message_indices=paging_calls,
                    suggested_fix="Consider parallel page fetching, larger page sizes, or cursor-based pagination",
                    estimated_improvement="30-50% improvement with optimized pagination"
                ))
        
        # Detect missing pagination (large data fetch without paging)
        fetch_keywords = ['get', 'fetch', 'load', 'query', 'select', 'all', 'list']
        for i, msg in enumerate(messages):
            message_lower = msg['message'].lower()
            has_fetch = any(kw in message_lower for kw in fetch_keywords)
            has_paging = any(kw in message_lower for kw in paging_keywords)
            has_large = any(kw in message_lower for kw in ['all', 'entire', 'complete', 'full'])
            
            if has_fetch and has_large and not has_paging:
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.PAGING,
                    severity=Severity.HIGH,
                    description="Paging issue: Large data fetch without pagination",
                    location={'message_index': i, 'message': msg['message']},
                    impact="Fetching large datasets without pagination can cause memory/performance issues",
                    affected_participants=[msg['from'], msg['to']],
                    message_indices=[i],
                    suggested_fix="Implement pagination with appropriate page size",
                    estimated_improvement="Prevents memory issues and improves response time"
                ))
    
    def _detect_bottlenecks(self, messages: List[Dict], participants: List[str]):
        """Detect bottleneck participants receiving too many calls."""
        participant_call_counts = defaultdict(int)
        
        for msg in messages:
            participant_call_counts[msg['to']] += 1
        
        # Identify bottlenecks (participants receiving disproportionate calls)
        total_calls = len(messages)
        avg_calls_per_participant = total_calls / len(participants) if participants else 0
        
        for participant, count in participant_call_counts.items():
            if count > avg_calls_per_participant * 2 and count >= 5:
                severity = Severity.CRITICAL if count >= 20 else Severity.HIGH if count >= 10 else Severity.MEDIUM
                
                self.issues.append(PerformanceIssue(
                    issue_type=IssueType.BOTTLENECK,
                    severity=severity,
                    description=f"Bottleneck detected: {participant} receives {count} calls ({count/total_calls*100:.1f}% of total)",
                    location={'participant': participant, 'call_count': count, 'percentage': count/total_calls*100},
                    impact=f"{participant} is a bottleneck causing performance degradation",
                    affected_participants=[participant],
                    message_indices=[i for i, msg in enumerate(messages) if msg['to'] == participant],
                    suggested_fix="Consider load balancing, caching, or optimizing this participant",
                    estimated_improvement="20-40% improvement by optimizing bottleneck"
                ))
    
    def _detect_long_chains(self, messages: List[Dict], participants: List[str]):
        """Detect long sequential chains that could be optimized."""
        if len(messages) < 5:
            return
        
        # Find longest chains
        max_chain_length = 0
        chain_start = 0
        
        current_chain = 1
        for i in range(len(messages) - 1):
            if messages[i]['to'] == messages[i+1]['from']:
                current_chain += 1
            else:
                if current_chain > max_chain_length:
                    max_chain_length = current_chain
                    chain_start = i - current_chain + 1
                current_chain = 1
        
        if current_chain > max_chain_length:
            max_chain_length = current_chain
            chain_start = len(messages) - current_chain
        
        if max_chain_length >= 5:
            self.issues.append(PerformanceIssue(
                issue_type=IssueType.LONG_CHAIN,
                severity=Severity.MEDIUM,
                description=f"Long chain detected: {max_chain_length} sequential calls",
                location={'chain_length': max_chain_length, 'start_index': chain_start},
                impact="Long sequential chain causing latency accumulation",
                affected_participants=list(set(messages[i]['to'] for i in range(chain_start, chain_start + max_chain_length))),
                message_indices=list(range(chain_start, chain_start + max_chain_length)),
                suggested_fix="Consider parallelizing independent operations or reducing chain length",
                estimated_improvement="20-30% improvement by reducing chain length"
            ))
    
    def _detect_round_trip_patterns(self, messages: List[Dict], participants: List[str]):
        """Detect excessive round-trip patterns."""
        round_trips = []
        
        for i in range(len(messages) - 1):
            msg1 = messages[i]
            msg2 = messages[i + 1]
            
            # Check for round-trip (A->B, B->A)
            if msg1['from'] == msg2['to'] and msg1['to'] == msg2['from']:
                round_trips.append((i, i+1))
        
        if len(round_trips) >= 3:
            self.issues.append(PerformanceIssue(
                issue_type=IssueType.ROUND_TRIP,
                severity=Severity.MEDIUM,
                description=f"Excessive round-trips: {len(round_trips)} detected",
                location={'round_trips': round_trips},
                impact="Multiple round-trips causing network latency accumulation",
                affected_participants=list(set(msg['from'] for trip in round_trips for msg in [messages[trip[0]], messages[trip[1]]])),
                message_indices=[idx for trip in round_trips for idx in trip],
                suggested_fix="Combine operations to reduce round-trips or use async operations",
                estimated_improvement="25-40% improvement by reducing round-trips"
            ))
    
    def _detect_missing_parallelization(self, messages: List[Dict], participants: List[str]):
        """Detect opportunities for parallelization."""
        parallel_opportunities = []
        
        # Look for independent calls from the same source
        for i in range(len(messages) - 1):
            msg1 = messages[i]
            msg2 = messages[i + 1]
            
            # If same source, different targets, and both synchronous
            if msg1['from'] == msg2['from'] and msg1['to'] != msg2['to'] and \
               not msg1.get('async') and not msg2.get('async'):
                parallel_opportunities.append((i, i+1))
        
        if len(parallel_opportunities) >= 2:
            self.issues.append(PerformanceIssue(
                issue_type=IssueType.MISSING_PARALLELIZATION,
                severity=Severity.LOW,
                description=f"Parallelization opportunity: {len(parallel_opportunities)} independent calls could run in parallel",
                location={'opportunities': parallel_opportunities},
                impact="Sequential execution of independent operations",
                affected_participants=list(set(msg['from'] for opp in parallel_opportunities for msg in [messages[opp[0]]])),
                message_indices=[idx for opp in parallel_opportunities for idx in opp],
                suggested_fix="Execute independent calls in parallel using async/await or parallel processing",
                estimated_improvement="30-50% improvement by parallelizing independent calls"
            ))
    
    def _generate_summary(self) -> Dict:
        """Generate summary of all detected issues."""
        if not self.issues:
            return {
                'status': 'clean',
                'message': 'No performance issues detected'
            }
        
        issue_counts = defaultdict(int)
        severity_counts = defaultdict(int)
        
        for issue in self.issues:
            issue_counts[issue.issue_type.value] += 1
            severity_counts[issue.severity.value] += 1
        
        return {
            'status': 'issues_detected',
            'total_issues': len(self.issues),
            'issue_breakdown': dict(issue_counts),
            'severity_breakdown': dict(severity_counts),
            'critical_issues': len([i for i in self.issues if i.severity == Severity.CRITICAL]),
            'high_priority_issues': len([i for i in self.issues if i.severity == Severity.HIGH]),
            'recommended_actions': len([i for i in self.issues if i.suggested_fix])
        }
    
    def _calculate_overall_risk(self) -> str:
        """Calculate overall risk level based on detected issues."""
        if not self.issues:
            return 'low'
        
        critical_count = len([i for i in self.issues if i.severity == Severity.CRITICAL])
        high_count = len([i for i in self.issues if i.severity == Severity.HIGH])
        
        if critical_count > 0:
            return 'critical'
        elif high_count >= 3:
            return 'high'
        elif high_count > 0 or len(self.issues) >= 5:
            return 'medium'
        else:
            return 'low'
    
    def _issue_to_dict(self, issue: PerformanceIssue) -> Dict:
        """Convert PerformanceIssue to dictionary."""
        return {
            'type': issue.issue_type.value,
            'severity': issue.severity.value,
            'description': issue.description,
            'location': issue.location,
            'impact': issue.impact,
            'affected_participants': issue.affected_participants,
            'message_indices': issue.message_indices,
            'suggested_fix': issue.suggested_fix,
            'estimated_improvement': issue.estimated_improvement
        }

