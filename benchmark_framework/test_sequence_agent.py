#!/usr/bin/env python3
"""Simple test script to verify the sequence diagram agent works."""

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent

def test_basic_functionality():
    """Test basic agent functionality."""
    print("Testing Sequence Diagram Agent...")
    
    # Simple test diagram
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: getOrders()
    API->>Database: SELECT * FROM orders
    Database-->>API: orders[]
    API-->>Client: orders[]
"""
    
    try:
        agent = SequenceDiagramAgent()
        result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
        
        print(f"[OK] Agent initialized successfully")
        print(f"[OK] Analysis completed")
        print(f"  - Total messages: {result.get('parsed_data', {}).get('total_messages', 0)}")
        print(f"  - Total issues: {result.get('analysis', {}).get('total_issues', 0)}")
        print(f"  - Risk level: {result.get('analysis', {}).get('risk_level', 'unknown')}")
        print(f"  - Total corrections: {result.get('corrections', {}).get('total_corrections', 0)}")
        
        # Test report generation
        report = agent.generate_report(format='text')
        print(f"[OK] Report generation works (length: {len(report)} chars)")
        
        print("\n[SUCCESS] All tests passed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)

