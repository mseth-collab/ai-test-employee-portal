# Sequence Diagram Analysis Agent

A comprehensive agent for parsing sequence diagrams, identifying performance issues, and generating corrections.

## Features

The agent can detect and correct the following performance issues:

- **Loopy Patterns**: Repeated calls that could be batched
- **Chatty Interfaces**: Too many small calls (N+1 problem)
- **Projection Issues**: Inefficient data fetching (fetch all then filter)
- **Paging Problems**: Sequential pagination or missing pagination
- **Bottlenecks**: Participants receiving disproportionate calls
- **Long Chains**: Excessive sequential call chains
- **Round-trips**: Excessive back-and-forth communication
- **Missing Parallelization**: Independent calls that could run in parallel

## Quick Start

### Basic Usage

```python
from benchmark_framework.core.sequence_diagram_agent import SequenceDiagramAgent

# Create agent
agent = SequenceDiagramAgent()

# Analyze a sequence diagram
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

result = agent.analyze_sequence_diagram(diagram, diagram_format="mermaid")

# Generate report
print(agent.generate_report(format='text'))
# or
print(agent.generate_report(format='markdown'))
# or
print(agent.generate_report(format='json'))
```

### Command Line Interface

```bash
# Analyze a diagram file
python benchmark_framework/run_sequence_analysis.py diagram.mmd

# Generate markdown report
python benchmark_framework/run_sequence_analysis.py diagram.mmd --output report.md --report-format markdown

# Filter by issue type
python benchmark_framework/run_sequence_analysis.py diagram.mmd --issue-type chatty

# Filter by severity
python benchmark_framework/run_sequence_analysis.py diagram.mmd --severity critical

# List only issues
python benchmark_framework/run_sequence_analysis.py diagram.mmd --list-issues

# List only corrections
python benchmark_framework/run_sequence_analysis.py diagram.mmd --list-corrections
```

## Supported Formats

- **Mermaid** (`.mmd` or auto-detected)
- **PlantUML** (`.puml` or auto-detected)

## Issue Types

### Loopy Patterns
Detects repeated patterns that could be optimized by batching.

**Example:**
```
Client->>Service: getItem(1)
Client->>Service: getItem(2)
Client->>Service: getItem(3)
...
```

**Correction:** Batch multiple calls into a single request.

### Chatty Interfaces (N+1 Problem)
Detects too many small calls, especially the classic N+1 query problem.

**Example:**
```
Client->>API: getOrders()
API->>Database: SELECT * FROM orders
Database-->>API: orders[]
API-->>Client: orders[]

loop For each order
    Client->>API: getOrderDetails(orderId)
    API->>Database: SELECT * FROM order_items WHERE order_id = ?
end
```

**Correction:** Use eager loading or joins to fetch all data in one query.

### Projection Issues
Detects inefficient data fetching patterns like fetching all data then filtering.

**Example:**
```
Client->>API: getAllProducts()
API->>Database: SELECT * FROM products
Database-->>API: allProducts[1000 items]
API->>API: filter(products, status='active')
API-->>Client: activeProducts[50 items]
```

**Correction:** Push filters to the data source (database/API).

### Paging Problems
Detects sequential pagination or missing pagination for large datasets.

**Example:**
```
Client->>API: getPage(1)
Client->>API: getPage(2)
Client->>API: getPage(3)
...
```

**Correction:** Use parallel page fetching or cursor-based pagination.

## API Reference

### SequenceDiagramAgent

Main agent class for analyzing sequence diagrams.

#### Methods

- `analyze_sequence_diagram(diagram_content, diagram_format="auto")` - Analyze a sequence diagram
- `analyze_sequence_diagram_file(file_path)` - Analyze from a file
- `get_issues_by_type(issue_type)` - Get issues of a specific type
- `get_issues_by_severity(severity)` - Get issues of a specific severity
- `get_corrections_for_issue_type(issue_type)` - Get corrections for an issue type
- `generate_report(format='text')` - Generate a human-readable report

### Issue Types

- `LOOPY` - Loopy patterns
- `CHATTY` - Chatty interfaces
- `PROJECTION` - Projection issues
- `PAGING` - Paging problems
- `BOTTLENECK` - Bottleneck participants
- `LONG_CHAIN` - Long sequential chains
- `ROUND_TRIP` - Round-trip patterns
- `MISSING_PARALLELIZATION` - Missing parallelization opportunities

### Severity Levels

- `CRITICAL` - Critical issues requiring immediate attention
- `HIGH` - High priority issues
- `MEDIUM` - Medium priority issues
- `LOW` - Low priority issues

## Examples

See `benchmark_framework/examples/sequence_diagram_analysis_example.py` for complete examples.

## Output Formats

### Text Report
Plain text format suitable for console output.

### Markdown Report
Markdown format suitable for documentation or GitHub.

### JSON Report
Structured JSON format for programmatic processing.

## Correction Strategies

The agent suggests various correction strategies:

- **Batching**: Combine multiple calls into batches
- **Caching**: Implement caching layers
- **Parallelization**: Execute independent calls in parallel
- **Join Optimization**: Use joins instead of multiple queries
- **Pagination Optimization**: Optimize pagination strategies
- **Architectural Change**: Suggest architectural improvements
- **Query Optimization**: Optimize queries and data fetching

## Integration

The agent can be integrated into CI/CD pipelines, code review processes, or used as a standalone analysis tool.

```python
# In CI/CD pipeline
agent = SequenceDiagramAgent()
result = agent.analyze_sequence_diagram_file("sequence_diagram.mmd")

if result['analysis']['risk_level'] in ['high', 'critical']:
    print("High risk issues detected!")
    sys.exit(1)
```

## Architecture

The agent consists of three main components:

1. **Parser** (`seqparser.py`) - Parses Mermaid and PlantUML sequence diagrams
2. **Analyzer** (`sequence_diagram_analyzer.py`) - Detects performance issues
3. **Correction Agent** (`correction_agent.py`) - Generates corrections and suggestions

## License

Part of the AI-SQLQuery Doctor benchmark framework.

