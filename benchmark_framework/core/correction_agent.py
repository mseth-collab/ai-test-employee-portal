"""
Sequence Diagram Correction Agent
=================================

This module provides an agent that can suggest and generate corrections
for performance issues detected in sequence diagrams.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from .sequence_diagram_analyzer import IssueType, PerformanceIssue, Severity


class CorrectionStrategy(Enum):
    """Strategies for correcting performance issues."""
    BATCHING = "batching"
    CACHING = "caching"
    PARALLELIZATION = "parallelization"
    JOIN_OPTIMIZATION = "join_optimization"
    PAGINATION_OPTIMIZATION = "pagination_optimization"
    ARCHITECTURAL_CHANGE = "architectural_change"
    QUERY_OPTIMIZATION = "query_optimization"


@dataclass
class Correction:
    """Represents a suggested correction for a performance issue."""
    issue_type: IssueType
    strategy: CorrectionStrategy
    description: str
    original_pattern: str
    corrected_pattern: str
    implementation_steps: List[str]
    code_example: Optional[str] = None
    expected_improvement: Optional[str] = None
    complexity: str = "medium"  # low, medium, high


class CorrectionAgent:
    """
    Agent that generates corrections for detected performance issues.
    """
    
    def __init__(self):
        self.corrections: List[Correction] = []
    
    def generate_corrections(self, analysis_result: Dict, parsed_data: Dict) -> Dict:
        """
        Generate corrections for all detected issues.
        
        Args:
            analysis_result: Result from SequenceDiagramAnalyzer.analyze()
            parsed_data: Original parsed sequence diagram data
            
        Returns:
            Dictionary containing all corrections
        """
        self.corrections = []
        issues = analysis_result.get('issues', [])
        messages = parsed_data.get('messages', [])
        
        for issue_dict in issues:
            issue_type = IssueType(issue_dict['type'])
            correction = self._generate_correction_for_issue(issue_type, issue_dict, messages)
            if correction:
                self.corrections.append(correction)
        
        return {
            'total_corrections': len(self.corrections),
            'corrections': [self._correction_to_dict(c) for c in self.corrections],
            'summary': self._generate_correction_summary()
        }
    
    def _generate_correction_for_issue(
        self, 
        issue_type: IssueType, 
        issue_dict: Dict, 
        messages: List[Dict]
    ) -> Optional[Correction]:
        """Generate correction for a specific issue type."""
        
        if issue_type == IssueType.LOOPY:
            return self._correct_loopy_pattern(issue_dict, messages)
        elif issue_type == IssueType.CHATTY:
            return self._correct_chatty_pattern(issue_dict, messages)
        elif issue_type == IssueType.PROJECTION:
            return self._correct_projection_issue(issue_dict, messages)
        elif issue_type == IssueType.PAGING:
            return self._correct_paging_issue(issue_dict, messages)
        elif issue_type == IssueType.BOTTLENECK:
            return self._correct_bottleneck(issue_dict, messages)
        elif issue_type == IssueType.LONG_CHAIN:
            return self._correct_long_chain(issue_dict, messages)
        elif issue_type == IssueType.ROUND_TRIP:
            return self._correct_round_trip(issue_dict, messages)
        elif issue_type == IssueType.MISSING_PARALLELIZATION:
            return self._correct_missing_parallelization(issue_dict, messages)
        
        return None
    
    def _correct_loopy_pattern(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for loopy patterns."""
        message_indices = issue_dict.get('message_indices', [])
        affected_messages = [messages[i] for i in message_indices[:5]]  # Take first 5 as example
        
        # Generate batched version
        from_participant = affected_messages[0]['from'] if affected_messages else 'Client'
        to_participant = affected_messages[0]['to'] if affected_messages else 'Service'
        
        original_pattern = '\n'.join([f"{msg['from']}->{msg['to']}: {msg['message']}" 
                                     for msg in affected_messages])
        
        corrected_pattern = f"{from_participant}->{to_participant}: batchRequest([{len(message_indices)} items])\n"
        corrected_pattern += f"{to_participant}-->>{from_participant}: batchResponse([results])"
        
        code_example = f"""
# Original (Loopy Pattern)
for item in items:
    result = service.get_item(item.id)  # N calls
    process(result)

# Corrected (Batched)
results = service.batch_get_items([item.id for item in items])  # 1 call
for result in results:
    process(result)
"""
        
        return Correction(
            issue_type=IssueType.LOOPY,
            strategy=CorrectionStrategy.BATCHING,
            description="Batch multiple calls into a single request",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Create a batch API endpoint that accepts multiple items",
                "2. Modify client code to collect items and send in batch",
                "3. Process batch on server side and return results",
                "4. Update client to handle batch response"
            ],
            code_example=code_example,
            expected_improvement="50-80% reduction in network calls and latency",
            complexity="medium"
        )
    
    def _correct_chatty_pattern(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for chatty patterns (N+1 problem)."""
        message_indices = issue_dict.get('message_indices', [])
        affected_messages = [messages[i] for i in message_indices[:3]]
        
        from_participant = affected_messages[0]['from'] if affected_messages else 'Client'
        to_participant = affected_messages[0]['to'] if affected_messages else 'Database'
        
        original_pattern = '\n'.join([f"{msg['from']}->{msg['to']}: {msg['message']}" 
                                     for msg in affected_messages])
        
        corrected_pattern = f"{from_participant}->{to_participant}: getItemsWithRelations(ids: [1..N])\n"
        corrected_pattern += f"{to_participant}-->>{from_participant}: itemsWithRelations"
        
        code_example = f"""
# Original (N+1 Problem)
items = get_items()  # 1 query
for item in items:
    item.details = get_item_details(item.id)  # N queries

# Corrected (Eager Loading / Join)
items = get_items_with_details()  # 1 query with JOIN
# All details loaded in single query
"""
        
        return Correction(
            issue_type=IssueType.CHATTY,
            strategy=CorrectionStrategy.JOIN_OPTIMIZATION,
            description="Use eager loading or joins to eliminate N+1 queries",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify the relationship between entities",
                "2. Modify query to use JOIN or eager loading",
                "3. Fetch all related data in a single query",
                "4. Update data access layer to support eager loading"
            ],
            code_example=code_example,
            expected_improvement="60-90% reduction in database queries",
            complexity="low"
        )
    
    def _correct_projection_issue(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for projection issues."""
        message_indices = issue_dict.get('message_indices', [])
        affected_messages = [messages[i] for i in message_indices[:2]]
        
        from_participant = affected_messages[0]['from'] if affected_messages else 'Client'
        to_participant = affected_messages[0]['to'] if affected_messages else 'Database'
        
        original_pattern = '\n'.join([f"{msg['from']}->{msg['to']}: {msg['message']}" 
                                     for msg in affected_messages])
        
        corrected_pattern = f"{from_participant}->{to_participant}: getFilteredData(filters: criteria)\n"
        corrected_pattern += f"{to_participant}-->>{from_participant}: filteredResults"
        
        code_example = """
# Original (Fetch All Then Filter)
all_data = database.get_all_items()  # Fetch everything
filtered = [item for item in all_data if item.status == 'active']  # Filter in memory

# Corrected (Filter at Source)
filtered = database.get_items(where={'status': 'active'})  # Filter in query
"""
        
        return Correction(
            issue_type=IssueType.PROJECTION,
            strategy=CorrectionStrategy.QUERY_OPTIMIZATION,
            description="Push filters to data source instead of fetching all data",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify filtering criteria",
                "2. Modify query to include WHERE clause or filters",
                "3. Remove client-side filtering logic",
                "4. Ensure proper indexing on filtered columns"
            ],
            code_example=code_example,
            expected_improvement="40-70% reduction in data transfer and processing",
            complexity="low"
        )
    
    def _correct_paging_issue(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for paging issues."""
        message_indices = issue_dict.get('message_indices', [])
        
        original_pattern = "Sequential page requests"
        corrected_pattern = "Parallel page requests or cursor-based pagination"
        
        code_example = f"""
# Original (Sequential Pagination)
for page in range(1, total_pages + 1):
    data = get_page(page)  # Sequential, slow
    process(data)

# Corrected Option 1 (Parallel)
import asyncio
async def fetch_all_pages():
    tasks = [get_page_async(page) for page in range(1, total_pages + 1)]
    results = await asyncio.gather(*tasks)  # Parallel, fast
    return results

# Corrected Option 2 (Cursor-based)
cursor = None
while True:
    data, cursor = get_page_cursor(cursor=cursor, limit=100)
    if not data:
        break
    process(data)
"""
        
        return Correction(
            issue_type=IssueType.PAGING,
            strategy=CorrectionStrategy.PAGINATION_OPTIMIZATION,
            description="Optimize pagination strategy",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Evaluate current pagination approach",
                "2. Consider parallel page fetching if pages are independent",
                "3. Implement cursor-based pagination for better performance",
                "4. Increase page size if appropriate",
                "5. Add caching for frequently accessed pages"
            ],
            code_example=code_example,
            expected_improvement="30-60% improvement in pagination performance",
            complexity="medium"
        )
    
    def _correct_bottleneck(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for bottleneck participants."""
        participant = issue_dict.get('location', {}).get('participant', 'Service')
        
        original_pattern = f"All calls go to {participant} (bottleneck)"
        corrected_pattern = f"Load balance or cache at {participant}"
        
        code_example = f"""
# Original (Single Bottleneck)
for request in requests:
    result = bottleneck_service.process(request)  # All through one service

# Corrected (Load Balanced)
from load_balancer import get_service_instance
for request in requests:
    service = get_service_instance()  # Distribute load
    result = service.process(request)

# Or with Caching
from cache import cache
@cache(ttl=300)
def process_with_cache(request):
    return bottleneck_service.process(request)
"""
        
        return Correction(
            issue_type=IssueType.BOTTLENECK,
            strategy=CorrectionStrategy.ARCHITECTURAL_CHANGE,
            description="Implement load balancing or caching for bottleneck",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify why this participant is a bottleneck",
                "2. Implement caching layer if data is cacheable",
                "3. Consider load balancing across multiple instances",
                "4. Optimize the bottleneck participant itself",
                "5. Consider horizontal scaling"
            ],
            code_example=code_example,
            expected_improvement="20-50% improvement by distributing load",
            complexity="high"
        )
    
    def _correct_long_chain(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for long chains."""
        chain_length = issue_dict.get('location', {}).get('chain_length', 5)
        
        original_pattern = f"Long chain of {chain_length} sequential calls"
        corrected_pattern = "Parallelize independent operations or reduce chain"
        
        code_example = f"""
# Original (Long Chain)
result1 = service1.process()
result2 = service2.process(result1)
result3 = service3.process(result2)
result4 = service4.process(result3)
result5 = service5.process(result4)

# Corrected (Parallelize Independent Operations)
result1 = service1.process()
# These can run in parallel
result2, result3 = await asyncio.gather(
    service2.process(result1),
    service3.process(result1)
)
# Continue with dependent operations
result4 = service4.process(result2, result3)
result5 = service5.process(result4)
"""
        
        return Correction(
            issue_type=IssueType.LONG_CHAIN,
            strategy=CorrectionStrategy.PARALLELIZATION,
            description="Parallelize independent operations in chain",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify independent operations in the chain",
                "2. Group operations that can run in parallel",
                "3. Use async/await or parallel processing",
                "4. Maintain dependencies between operations",
                "5. Test for race conditions"
            ],
            code_example=code_example,
            expected_improvement="20-40% improvement by parallelizing",
            complexity="medium"
        )
    
    def _correct_round_trip(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for round-trip patterns."""
        original_pattern = "Multiple round-trips (A->B, B->A)"
        corrected_pattern = "Combine operations to reduce round-trips"
        
        code_example = f"""
# Original (Round-trips)
result = service.get_data(id)
service.update_status(id, 'processing')
result = service.get_data(id)  # Another round-trip

# Corrected (Combined)
result = service.get_and_update(id, status='processing')  # Single call
"""
        
        return Correction(
            issue_type=IssueType.ROUND_TRIP,
            strategy=CorrectionStrategy.ARCHITECTURAL_CHANGE,
            description="Combine operations to reduce round-trips",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify operations that cause round-trips",
                "2. Design combined API methods",
                "3. Update client to use combined methods",
                "4. Consider using transactions for related operations"
            ],
            code_example=code_example,
            expected_improvement="30-50% reduction in network latency",
            complexity="low"
        )
    
    def _correct_missing_parallelization(self, issue_dict: Dict, messages: List[Dict]) -> Correction:
        """Generate correction for missing parallelization."""
        original_pattern = "Sequential independent calls"
        corrected_pattern = "Parallel execution of independent calls"
        
        code_example = f"""
# Original (Sequential)
result1 = service1.get_data()
result2 = service2.get_data()
result3 = service3.get_data()

# Corrected (Parallel)
import asyncio
results = await asyncio.gather(
    service1.get_data_async(),
    service2.get_data_async(),
    service3.get_data_async()
)
result1, result2, result3 = results
"""
        
        return Correction(
            issue_type=IssueType.MISSING_PARALLELIZATION,
            strategy=CorrectionStrategy.PARALLELIZATION,
            description="Execute independent calls in parallel",
            original_pattern=original_pattern,
            corrected_pattern=corrected_pattern,
            implementation_steps=[
                "1. Identify independent operations",
                "2. Convert to async methods if not already",
                "3. Use asyncio.gather() or similar for parallel execution",
                "4. Handle errors appropriately",
                "5. Test concurrent behavior"
            ],
            code_example=code_example,
            expected_improvement="30-60% improvement by parallelizing",
            complexity="low"
        )
    
    def _generate_correction_summary(self) -> Dict:
        """Generate summary of corrections."""
        if not self.corrections:
            return {'message': 'No corrections generated'}
        
        strategy_counts = {}
        complexity_counts = {}
        
        for correction in self.corrections:
            strategy_counts[correction.strategy.value] = strategy_counts.get(correction.strategy.value, 0) + 1
            complexity_counts[correction.complexity] = complexity_counts.get(correction.complexity, 0) + 1
        
        return {
            'total_corrections': len(self.corrections),
            'strategy_breakdown': strategy_counts,
            'complexity_breakdown': complexity_counts,
            'low_complexity': complexity_counts.get('low', 0),
            'medium_complexity': complexity_counts.get('medium', 0),
            'high_complexity': complexity_counts.get('high', 0)
        }
    
    def _correction_to_dict(self, correction: Correction) -> Dict:
        """Convert Correction to dictionary."""
        return {
            'issue_type': correction.issue_type.value,
            'strategy': correction.strategy.value,
            'description': correction.description,
            'original_pattern': correction.original_pattern,
            'corrected_pattern': correction.corrected_pattern,
            'implementation_steps': correction.implementation_steps,
            'code_example': correction.code_example,
            'expected_improvement': correction.expected_improvement,
            'complexity': correction.complexity
        }

