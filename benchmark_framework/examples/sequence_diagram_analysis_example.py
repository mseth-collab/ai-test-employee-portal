"""
Example: Sequence Diagram Analysis Agent
=========================================

This example demonstrates how to use the Sequence Diagram Analysis Agent
to identify performance issues and generate corrections.
"""

from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent


def example_mermaid_diagram():
    """Example with a Mermaid sequence diagram showing N+1 problem."""
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: getOrders()
    API->>Database: SELECT * FROM orders
    Database-->>API: orders[]
    API-->>Client: orders[]
    
    loop For each order
        Client->>API: getOrderDetails(orderId)
        API->>Database: SELECT * FROM order_items WHERE order_id = ?
        Database-->>API: items[]
        API-->>Client: items[]
    end
"""
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("=" * 80)
    print("EXAMPLE 1: Mermaid Diagram with N+1 Problem")
    print("=" * 80)
    print(agent.generate_report(format='text'))
    print("\n")


def example_plantuml_diagram():
    """Example with a PlantUML sequence diagram showing loopy pattern."""
    diagram = """
@startuml
participant Client
participant Service
participant Database

Client -> Service: processItems()
Service -> Database: getItem(1)
Database --> Service: item1
Service -> Database: getItem(2)
Database --> Service: item2
Service -> Database: getItem(3)
Database --> Service: item3
Service -> Database: getItem(4)
Database --> Service: item4
Service -> Database: getItem(5)
Database --> Service: item5
Service --> Client: processed
@enduml
"""
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="plantuml")
    
    print("=" * 80)
    print("EXAMPLE 2: PlantUML Diagram with Loopy Pattern")
    print("=" * 80)
    print(agent.generate_report(format='text'))
    print("\n")


def example_chatty_interface():
    """Example showing a chatty interface pattern."""
    diagram = """
sequenceDiagram
    participant Frontend
    participant Backend
    participant Cache
    participant Database
    
    Frontend->>Backend: getUser(1)
    Backend->>Cache: get(user:1)
    Cache-->>Backend: null
    Backend->>Database: SELECT * FROM users WHERE id=1
    Database-->>Backend: user1
    Backend-->>Frontend: user1
    
    Frontend->>Backend: getUser(2)
    Backend->>Cache: get(user:2)
    Cache-->>Backend: null
    Backend->>Database: SELECT * FROM users WHERE id=2
    Database-->>Backend: user2
    Backend-->>Frontend: user2
    
    Frontend->>Backend: getUser(3)
    Backend->>Cache: get(user:3)
    Cache-->>Backend: null
    Backend->>Database: SELECT * FROM users WHERE id=3
    Database-->>Backend: user3
    Backend-->>Frontend: user3
"""
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("=" * 80)
    print("EXAMPLE 3: Chatty Interface Pattern")
    print("=" * 80)
    print(agent.generate_report(format='markdown'))
    print("\n")


def example_projection_issue():
    """Example showing projection issue (fetch all then filter)."""
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: getAllProducts()
    API->>Database: SELECT * FROM products
    Database-->>API: allProducts[1000 items]
    API->>API: filter(products, status='active')
    API-->>Client: activeProducts[50 items]
"""
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("=" * 80)
    print("EXAMPLE 4: Projection Issue (Fetch All Then Filter)")
    print("=" * 80)
    print(agent.generate_report(format='text'))
    print("\n")


def example_paging_issue():
    """Example showing paging issues."""
    diagram = """
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: getPage(1)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 0
    Database-->>API: page1
    API-->>Client: page1
    
    Client->>API: getPage(2)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 10
    Database-->>API: page2
    API-->>Client: page2
    
    Client->>API: getPage(3)
    API->>Database: SELECT * FROM items LIMIT 10 OFFSET 20
    Database-->>API: page3
    API-->>Client: page3
"""
    
    agent = SequenceDiagramAgent()
    result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")
    
    print("=" * 80)
    print("EXAMPLE 5: Paging Issue (Sequential Pagination)")
    print("=" * 80)
    print(agent.generate_report(format='text'))
    print("\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("SEQUENCE DIAGRAM ANALYSIS AGENT - EXAMPLES")
    print("=" * 80 + "\n")
    
    try:
        example_mermaid_diagram()
        example_plantuml_diagram()
        example_chatty_interface()
        example_projection_issue()
        example_paging_issue()
        
        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80 + "\n")
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

