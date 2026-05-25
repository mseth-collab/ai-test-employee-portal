import re
import json
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

def parse_mermaid_sequence(content: str) -> Dict:
    """
    Parse Mermaid sequence diagram syntax and extract components, messages, and flow.
    Returns structured data for analysis.
    """
    participants = []
    messages = []
    activations = []
    
    lines = content.strip().split('\n')
    in_sequence = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
            
        # Check if sequence diagram
        if 'sequenceDiagram' in line:
            in_sequence = True
            continue
            
        if not in_sequence:
            continue
            
        # Parse participants
        if line.startswith('participant'):
            match = re.search(r'participant\s+(\w+)', line)
            if match:
                participants.append(match.group(1))
        
        # Parse messages (arrows)
        arrow_pattern = r'(\w+)\s*([->>]+|->|-->>|-->)\s*(\w+)\s*:\s*(.+)'
        match = re.match(arrow_pattern, line)
        if match:
            from_actor = match.group(1)
            arrow = match.group(2)
            to_actor = match.group(3)
            message = match.group(4)
            
            is_async = '>>' in arrow or '--' in arrow
            messages.append({
                'from': from_actor,
                'to': to_actor,
                'message': message,
                'async': is_async,
                'line': line
            })
    
    return {
        'participants': participants,
        'messages': messages,
        'total_messages': len(messages),
        'total_participants': len(participants)
    }


def parse_plantuml_sequence(content: str) -> Dict:
    """
    Parse PlantUML sequence diagram syntax.
    """
    participants = []
    messages = []
    
    lines = content.strip().split('\n')
    in_sequence = False
    
    for line in lines:
        line = line.strip()
        if '@startuml' in line or 'sequence' in line.lower():
            in_sequence = True
            continue
        if '@enduml' in line:
            break
            
        if not in_sequence:
            continue
            
        # Parse participants
        if line.startswith('participant') or line.startswith('actor'):
            match = re.search(r'(?:participant|actor)\s+(\w+)', line)
            if match:
                participants.append(match.group(1))
        
        # Parse messages
        arrow_pattern = r'(\w+)\s*([->]+|-->|->>)\s*(\w+)\s*:\s*(.+)'
        match = re.match(arrow_pattern, line)
        if match:
            from_actor = match.group(1)
            arrow = match.group(2)
            to_actor = match.group(3)
            message = match.group(4)
            
            is_async = '>>' in arrow or '--' in arrow
            messages.append({
                'from': from_actor,
                'to': to_actor,
                'message': message,
                'async': is_async,
                'line': line
            })
    
    return {
        'participants': participants,
        'messages': messages,
        'total_messages': len(messages),
        'total_participants': len(participants)
    }


def analyze_sequence_performance(parsed_data: Dict) -> Dict:
    """
    Analyze sequence diagram for performance bottlenecks.
    Returns data points and potential issues.
    """
    messages = parsed_data.get('messages', [])
    participants = parsed_data.get('participants', [])
    
    # Data points for analysis
    data_points = {
        'total_messages': len(messages),
        'synchronous_calls': 0,
        'asynchronous_calls': 0,
        'sequential_chains': [],
        'potential_parallelization': [],
        'long_chains': [],
        'back_and_forth_patterns': [],
        'bottleneck_participants': defaultdict(int)
    }
    
    # Analyze each message
    for msg in messages:
        if msg.get('async'):
            data_points['asynchronous_calls'] += 1
        else:
            data_points['synchronous_calls'] += 1
            data_points['bottleneck_participants'][msg['to']] += 1
    
    # Find sequential chains (A->B->C->D)
    if len(messages) > 1:
        for i in range(len(messages) - 1):
            if messages[i]['to'] == messages[i+1]['from']:
                chain_length = 2
                j = i + 1
                while j < len(messages) - 1 and messages[j]['to'] == messages[j+1]['from']:
                    chain_length += 1
                    j += 1
                if chain_length >= 3:
                    data_points['long_chains'].append({
                        'start': messages[i]['from'],
                        'length': chain_length,
                        'messages': [m['message'] for m in messages[i:i+chain_length]]
                    })
    
    # Find back-and-forth patterns (A->B, B->A, A->B)
    for i in range(len(messages) - 2):
        msg1 = messages[i]
        msg2 = messages[i+1]
        msg3 = messages[i+2] if i+2 < len(messages) else None
        
        if msg3 and msg1['from'] == msg2['to'] == msg3['from'] and \
           msg1['to'] == msg2['from'] == msg3['to']:
            data_points['back_and_forth_patterns'].append({
                'participants': [msg1['from'], msg1['to']],
                'round_trips': 3
            })
    
    # Find potential parallelization opportunities
    # Look for independent calls that could run in parallel
    for i in range(len(messages) - 1):
        msg1 = messages[i]
        msg2 = messages[i+1]
        
        # If two messages go to different participants from the same source
        if msg1['from'] == msg2['from'] and msg1['to'] != msg2['to']:
            if not msg1.get('async') and not msg2.get('async'):
                data_points['potential_parallelization'].append({
                    'from': msg1['from'],
                    'to': [msg1['to'], msg2['to']],
                    'messages': [msg1['message'], msg2['message']]
                })
    
    # Calculate bottleneck score
    bottleneck_scores = dict(data_points['bottleneck_participants'])
    max_bottleneck = max(bottleneck_scores.values()) if bottleneck_scores else 0
        
    data_points['bottleneck_score'] = max_bottleneck
    data_points['sync_ratio'] = data_points['synchronous_calls'] / len(messages) if messages else 0
    
    return data_points


def extract_performance_metrics(parsed_data: Dict, performance_data: Dict) -> Dict:
    """
    Extract key performance metrics from the analysis.
    """
    return {
        'total_interactions': performance_data['total_messages'],
        'synchronous_ratio': performance_data['sync_ratio'],
        'longest_chain': max([c['length'] for c in performance_data['long_chains']], default=0),
        'parallelization_opportunities': len(performance_data['potential_parallelization']),
        'round_trip_patterns': len(performance_data['back_and_forth_patterns']),
        'bottleneck_participant': max(performance_data['bottleneck_participants'].items(), 
                                      key=lambda x: x[1], default=(None, 0))[0],
        'bottleneck_score': performance_data['bottleneck_score'],
        'risk_level': 'high' if performance_data['sync_ratio'] > 0.7 else 
                     'medium' if performance_data['sync_ratio'] > 0.4 else 'low'
    }


# Convenience function for quick analysis
def analyze_sequence_diagram(diagram_content: str, diagram_format: str = "auto") -> Dict:
    """
    Quick analysis function that uses the full agent pipeline.
    
    Args:
        diagram_content: Content of the sequence diagram
        diagram_format: Format ("mermaid", "plantuml", or "auto")
        
    Returns:
        Complete analysis result with issues and corrections
    """
    from .sequence_diagram_agent import SequenceDiagramAgent
    
    agent = SequenceDiagramAgent()
    return agent.analyze_sequence_diagram(diagram_content, diagram_format)