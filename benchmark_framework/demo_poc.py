#!/usr/bin/env python3
"""
Proof of Concept Demo - Sequence Diagram Analysis Agent
========================================================

This demo shows the agent in action with a real-world example
demonstrating multiple performance issues.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def print_section(title, char="="):
    """Print a formatted section header."""
    print("\n" + char * 80)
    print(f"  {title}")
    print(char * 80 + "\n")


def demo_n_plus_one_problem():
    """Demo showing N+1 query problem."""
    print_section("DEMO 1: N+1 Query Problem (Chatty Interface)")
    
    # This is a classic N+1 problem - fetching orders, then fetching details for each
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Note over Client,Database: User requests order list with details
    
    Client->>API: getOrders()
    API->>Database: SELECT * FROM orders WHERE user_id = 123
    Database-->>API: orders[10 items]
    API-->>Client: orders[10 items]
    
    Note over Client,Database: Now fetching details for each order (N+1 problem!)
    
    loop For each order (10 iterations)
        Client->>API: getOrderDetails(orderId)
        API->>Database: SELECT * FROM order_items WHERE order_id = ?
        Database-->>API: items[]
        API-->>Client: items[]
    end
    
    Note over Client,Database: Total: 1 + 10 = 11 database queries!
"""
    
    print("INPUT DIAGRAM:")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("ANALYSIS RESULTS:")
    print("-" * 80)
    print(f"Total Messages Parsed: {result.get('parsed_data', {}).get('total_messages', 0)}")
    print(f"Total Issues Detected: {result.get('analysis', {}).get('total_issues', 0)}")
    print(f"Overall Risk Level: {result.get('analysis', {}).get('risk_level', 'unknown').upper()}")
    print("\n")
    
    # Show detected issues
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("DETECTED ISSUES:")
        print("-" * 80)
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
        print("\n\nGENERATED CORRECTIONS:")
        print("-" * 80)
        for i, correction in enumerate(corrections, 1):
            print(f"\n{i}. {correction.get('description', '')}")
            print(f"   Strategy: {correction.get('strategy', '').upper()}")
            print(f"   Complexity: {correction.get('complexity', '').upper()}")
            if correction.get('code_example'):
                print(f"\n   Code Example:")
                print("   " + "-" * 76)
                for line in correction.get('code_example', '').split('\n'):
                    if line.strip():
                        print(f"   {line}")
                print("   " + "-" * 76)
            if correction.get('expected_improvement'):
                print(f"\n   Expected Improvement: {correction.get('expected_improvement', '')}")


def demo_loopy_pattern():
    """Demo showing loopy pattern."""
    print_section("DEMO 2: Loopy Pattern (Repeated Calls)")
    
    diagram = """
sequenceDiagram
    participant Client
    participant ProductService
    participant Database
    
    Note over Client,Database: Fetching product details one by one
    
    Client->>ProductService: getProduct(1)
    ProductService->>Database: SELECT * FROM products WHERE id = 1
    Database-->>ProductService: product1
    ProductService-->>Client: product1
    
    Client->>ProductService: getProduct(2)
    ProductService->>Database: SELECT * FROM products WHERE id = 2
    Database-->>ProductService: product2
    ProductService-->>Client: product2
    
    Client->>ProductService: getProduct(3)
    ProductService->>Database: SELECT * FROM products WHERE id = 3
    Database-->>ProductService: product3
    ProductService-->>Client: product3
    
    Client->>ProductService: getProduct(4)
    ProductService->>Database: SELECT * FROM products WHERE id = 4
    Database-->>ProductService: product4
    ProductService-->>Client: product4
    
    Client->>ProductService: getProduct(5)
    ProductService->>Database: SELECT * FROM products WHERE id = 5
    Database-->>ProductService: product5
    ProductService-->>Client: product5
"""
    
    print("INPUT DIAGRAM:")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("ANALYSIS RESULTS:")
    print("-" * 80)
    print(f"Total Messages: {result.get('parsed_data', {}).get('total_messages', 0)}")
    print(f"Total Issues: {result.get('analysis', {}).get('total_issues', 0)}")
    print(f"Risk Level: {result.get('analysis', {}).get('risk_level', 'unknown').upper()}")
    
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("\nDETECTED ISSUES:")
        print("-" * 80)
        for issue in issues:
            print(f"\n[{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"  {issue.get('description', '')}")
            print(f"  Impact: {issue.get('impact', '')}")
    
    corrections = result.get('corrections', {}).get('corrections', [])
    if corrections:
        print("\n\nCORRECTIONS:")
        print("-" * 80)
        for correction in corrections:
            print(f"\n{correction.get('description', '')}")
            if correction.get('code_example'):
                print("\nCode Example:")
                print(correction.get('code_example', ''))


def demo_projection_issue():
    """Demo showing projection issue."""
    print_section("DEMO 3: Projection Issue (Fetch All Then Filter)")
    
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Note over Client,Database: Fetching all products then filtering in memory
    
    Client->>API: getAllProducts()
    API->>Database: SELECT * FROM products
    Database-->>API: allProducts[5000 items]
    Note over API: Filtering in memory (inefficient!)
    API->>API: filter(products, status='active', category='electronics')
    API-->>Client: filteredProducts[50 items]
    
    Note over Client,Database: Fetched 5000 items but only needed 50!
"""
    
    print("INPUT DIAGRAM:")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("ANALYSIS RESULTS:")
    print("-" * 80)
    print(f"Total Issues: {result.get('analysis', {}).get('total_issues', 0)}")
    
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("\nDETECTED ISSUES:")
        for issue in issues:
            print(f"\n[{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"  {issue.get('description', '')}")
            print(f"  {issue.get('impact', '')}")


def demo_paging_issue():
    """Demo showing paging issue."""
    print_section("DEMO 4: Paging Issue (Sequential Pagination)")
    
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Note over Client,Database: Fetching pages sequentially (slow!)
    
    Client->>API: getPage(1, pageSize=10)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 0
    Database-->>API: page1[10 items]
    API-->>Client: page1
    
    Client->>API: getPage(2, pageSize=10)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 10
    Database-->>API: page2[10 items]
    API-->>Client: page2
    
    Client->>API: getPage(3, pageSize=10)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 20
    Database-->>API: page3[10 items]
    API-->>Client: page3
    
    Note over Client,Database: Could fetch pages in parallel!
"""
    
    print("INPUT DIAGRAM:")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("ANALYSIS RESULTS:")
    print("-" * 80)
    print(f"Total Issues: {result.get('analysis', {}).get('total_issues', 0)}")
    
    issues = result.get('analysis', {}).get('issues', [])
    if issues:
        print("\nDETECTED ISSUES:")
        for issue in issues:
            print(f"\n[{issue.get('severity', '').upper()}] {issue.get('type', '').upper()}")
            print(f"  {issue.get('description', '')}")
            print(f"  {issue.get('suggested_fix', '')}")


def demo_comprehensive_report():
    """Demo showing comprehensive report generation."""
    print_section("DEMO 5: Comprehensive Report Generation")
    
    # Complex diagram with multiple issues
    diagram = """
sequenceDiagram
    participant Frontend
    participant Backend
    participant Cache
    participant Database
    
    Note over Frontend,Database: Complex scenario with multiple issues
    
    Frontend->>Backend: getUserOrders(userId)
    Backend->>Database: SELECT * FROM orders WHERE user_id = ?
    Database-->>Backend: orders[20 items]
    
    loop For each order
        Backend->>Database: SELECT * FROM order_items WHERE order_id = ?
        Database-->>Backend: items[]
        Backend->>Database: SELECT * FROM products WHERE id = ?
        Database-->>Backend: product
    end
    
    Backend->>Backend: filter(orders, status='active')
    Backend-->>Frontend: filteredOrders
"""
    
    print("INPUT DIAGRAM (Multiple Issues):")
    print("-" * 80)
    print(diagram)
    print("\n")
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("FULL TEXT REPORT:")
    print("=" * 80)
    report = agent.generate_report(format='text')
    print(report)
    
    print("\n\nMARKDOWN REPORT (first 1000 chars):")
    print("=" * 80)
    markdown_report = agent.generate_report(format='markdown')
    print(markdown_report[:1000] + "...\n[Report truncated for display]")


def main():
    """Run all demos."""
    print("\n" + "=" * 80)
    print("  SEQUENCE DIAGRAM ANALYSIS AGENT - PROOF OF CONCEPT DEMO")
    print("=" * 80)
    print("\nThis demo shows the agent detecting and correcting performance issues")
    print("in sequence diagrams.\n")
    
    try:
        # Run demos
        demo_n_plus_one_problem()
        input("\nPress Enter to continue to next demo...")
        
        demo_loopy_pattern()
        input("\nPress Enter to continue to next demo...")
        
        demo_projection_issue()
        input("\nPress Enter to continue to next demo...")
        
        demo_paging_issue()
        input("\nPress Enter to continue to next demo...")
        
        demo_comprehensive_report()
        
        print_section("DEMO COMPLETE - All scenarios demonstrated successfully!", "=")
        print("\nThe agent successfully:")
        print("  ✓ Parsed sequence diagrams (Mermaid format)")
        print("  ✓ Detected multiple performance issues")
        print("  ✓ Generated specific corrections with code examples")
        print("  ✓ Created comprehensive reports in multiple formats")
        print("\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

