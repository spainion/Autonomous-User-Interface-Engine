# Workflow Database System

## Overview

The Workflow Database System provides a comprehensive catalog of all system components, workflows, agents, and files. It enables intelligent workflow planning, session continuity, and knowledge preservation across multiple sessions.

## Features

### 1. **Complete System Cataloging**
- Automatic repository scanning
- File metadata tracking (checksums, types, purposes)
- Dependency mapping
- Component relationship tracking

### 2. **Agent Registration & Management**
- Agent capability registration
- Workflow-agent mapping
- Performance metrics tracking
- Dynamic agent discovery

### 3. **Workflow Definition & Execution**
- Structured workflow definitions
- Step-by-step execution plans
- Required agent specification
- Success rate tracking

### 4. **Session Continuity**
- Session memory preservation
- Context snapshots
- Agent state persistence
- Workflow progress tracking
- Learned pattern storage

### 5. **Knowledge Graph**
- File-component relationships
- Workflow-agent dependencies
- Cross-reference tracking
- Intelligent querying

## Quick Start

### Basic Usage

```python
from workflow_database import WorkflowDatabase, initialize_default_workflows

# Initialize database
db = WorkflowDatabase()

# Scan repository
stats = db.scan_repository()
print(f"Scanned {stats['total_files']} files")

# Register agents
db.register_agent('codex', {
    'description': 'Code generation agent',
    'capabilities': ['code_generation', 'code_review']
})

# Initialize default workflows
initialize_default_workflows(db)

# Build knowledge graph
db.build_knowledge_graph()

# Generate report
report = db.generate_report()
print(report)

# Export database
db.export_database("workflow_db.json")
```

### Defining Custom Workflows

```python
from workflow_database import WorkflowDefinition

# Define a workflow
custom_workflow = WorkflowDefinition(
    workflow_id="custom_task",
    name="Custom Task Workflow",
    description="Performs custom task processing",
    steps=[
        {'step': 1, 'action': 'Analyze input', 'agent': 'reasoning'},
        {'step': 2, 'action': 'Generate solution', 'agent': 'codex'},
        {'step': 3, 'action': 'Validate output', 'agent': 'reasoning'}
    ],
    required_agents=['reasoning', 'codex'],
    input_requirements={'text': 'string', 'context': 'dict'},
    output_format={'result': 'string', 'confidence': 'float'},
    estimated_time=25.0,
    success_rate=0.90
)

db.define_workflow(custom_workflow)
```

### Session Management

```python
from workflow_database import SessionMemory

# Create session memory
session = SessionMemory(
    session_id="session_123",
    timestamp=datetime.now().isoformat(),
    context_snapshot={'key': 'value'},
    agent_states={'codex': {'ready': True}},
    workflow_progress={'ui_generation': 0.75},
    learned_patterns=['pattern1', 'pattern2']
)

# Save session
db.save_session(session)

# Restore session later
restored = db.restore_session("session_123")
if restored:
    print(f"Restored session from {restored.timestamp}")
```

## Data Structures

### FileMetadata

```python
@dataclass
class FileMetadata:
    path: str                       # Relative path from repo root
    file_type: str                  # Type classification
    purpose: str                    # Description of purpose
    dependencies: List[str]         # List of dependent files
    related_agents: List[str]       # Agents that use this file
    last_modified: str             # ISO timestamp
    size_bytes: int                # File size
    checksum: str                  # SHA-256 checksum (first 16 chars)
```

### AgentCapability

```python
@dataclass
class AgentCapability:
    name: str                      # Capability name
    description: str               # What it does
    input_types: List[str]         # Accepted input types
    output_types: List[str]        # Produced output types
    required_context: List[str]    # Required context
    performance_metrics: Dict      # Performance data
```

### WorkflowDefinition

```python
@dataclass
class WorkflowDefinition:
    workflow_id: str               # Unique identifier
    name: str                      # Display name
    description: str               # Purpose description
    steps: List[Dict]              # Ordered execution steps
    required_agents: List[str]     # Agents needed
    input_requirements: Dict       # Required inputs
    output_format: Dict            # Output structure
    estimated_time: float          # Average execution time (seconds)
    success_rate: float            # Historical success rate (0-1)
```

### SessionMemory

```python
@dataclass
class SessionMemory:
    session_id: str                # Session identifier
    timestamp: str                 # Creation timestamp
    context_snapshot: Dict         # Full context at save time
    agent_states: Dict             # State of each agent
    workflow_progress: Dict        # Progress per workflow
    learned_patterns: List[str]    # New patterns learned
```

## API Reference

### WorkflowDatabase Class

#### `__init__(base_path: str = None)`
Initialize database with optional custom base path.

#### `scan_repository() -> Dict[str, Any]`
Scan entire repository and catalog all files.

**Returns:** Statistics dictionary with counts and totals

#### `register_agent(agent_name: str, agent_info: Dict[str, Any])`
Register an agent and its capabilities.

**Parameters:**
- `agent_name`: Unique agent identifier
- `agent_info`: Dictionary with description and capabilities

#### `define_workflow(workflow: WorkflowDefinition)`
Add a workflow definition to the database.

#### `save_session(session: SessionMemory)`
Save session memory for future restoration.

#### `restore_session(session_id: str) -> Optional[SessionMemory]`
Restore a previously saved session.

#### `build_knowledge_graph()`
Build knowledge graph connecting files, agents, and workflows.

#### `get_agent_workflows(agent_name: str) -> List[WorkflowDefinition]`
Get all workflows that use a specific agent.

#### `get_related_files(file_path: str, max_depth: int = 2) -> List[str]`
Get files related through dependencies or type.

#### `export_database(output_path: str = "workflow_database.json") -> str`
Export database to JSON file.

**Returns:** Path to exported file

#### `import_database(input_path: str)`
Import database from JSON file.

#### `generate_report() -> str`
Generate comprehensive text report of entire system.

## Default Workflows

### UI Generation Workflow

**ID:** `ui_generation`  
**Purpose:** Convert natural language to complete UI implementations

**Steps:**
1. Parse NLP input (nlp_interpreter)
2. Design UI structure (ui_designer)
3. Generate code (codex)
4. Validate & enhance (reasoning)

**Estimated Time:** 30 seconds  
**Success Rate:** 92%

### Code Enhancement Workflow

**ID:** `code_enhancement`  
**Purpose:** Analyze and enhance existing code

**Steps:**
1. Analyze code (codex)
2. Identify improvements (reasoning)
3. Apply enhancements (codex)
4. Validate changes (reasoning)

**Estimated Time:** 20 seconds  
**Success Rate:** 88%

### Multi-Agent Collaboration Workflow

**ID:** `multi_agent_collaboration`  
**Purpose:** Coordinate multiple agents for complex problems

**Steps:**
1. Decompose problem (reasoning)
2. Assign subtasks (reasoning)
3. Execute in parallel (all agents)
4. Integrate results (reasoning)

**Estimated Time:** 45 seconds  
**Success Rate:** 85%

## Knowledge Graph Structure

The knowledge graph connects:

- **Files ↔ Components**: Which files belong to which system components
- **Workflows ↔ Agents**: Which agents are required for each workflow
- **Agents ↔ Capabilities**: What each agent can do
- **Sessions ↔ Context**: Session history and learned patterns

### Querying the Knowledge Graph

```python
# Get all files for a component
agent_files = db.knowledge_graph.get('agent', set())

# Get workflow dependencies
workflow_deps = db.knowledge_graph.get('workflow_dependencies', set())

# Find related files
related = db.get_related_files('agents/codex.py')
```

## Integration with Other Systems

### With Context Engine

```python
from agent_init import init_agent_system
from workflow_database import WorkflowDatabase

# Initialize both systems
engine, agents = init_agent_system()
db = WorkflowDatabase()

# Register agents from system
for agent_name, agent in agents.items():
    db.register_agent(agent_name, {
        'description': f'{agent_name} agent',
        'type': agent.__class__.__name__
    })

# Store workflow results in context
result = agents['codex'].generate_code("task")
engine.add_node(
    content=json.dumps(result),
    node_type='workflow_result',
    metadata={'workflow': 'code_generation'}
)
```

### With NLP System

```python
from enhanced_nlp_system import EnhancedNLPSystem
from workflow_database import WorkflowDatabase

nlp = EnhancedNLPSystem()
db = WorkflowDatabase()

# Interpret and route to workflow
interpretation = nlp.interpret_with_context("Create a dashboard")

# Select workflow based on intent
if interpretation.intent.value == 'create_ui':
    workflow = db.workflows.get('ui_generation')
    # Execute workflow
```

## Best Practices

### 1. Regular Repository Scans

```python
# Scan regularly to track changes
db.scan_repository()

# Re-scan after significant changes
# This updates checksums and detects new files
```

### 2. Session Persistence

```python
# Save session at regular intervals
session = SessionMemory(...)
db.save_session(session)

# Export database periodically
db.export_database("backup_" + datetime.now().strftime("%Y%m%d") + ".json")
```

### 3. Workflow Metrics

```python
# Update success rates after execution
workflow.success_rate = (workflow.success_rate * 0.9) + (new_success * 0.1)

# Track execution times
workflow.estimated_time = moving_average(execution_times)
```

### 4. Knowledge Graph Maintenance

```python
# Rebuild after major changes
db.build_knowledge_graph()

# Query to find optimization opportunities
related_files = db.get_related_files('critical_file.py')
# Optimize these files together
```

## Performance Considerations

- **Repository Scanning**: O(n) where n = number of files
  - First scan: ~2-5 seconds for 100 files
  - Incremental updates possible with checksum comparison

- **Knowledge Graph**: O(n + m) where n = nodes, m = edges
  - Building: ~1 second for 1000 nodes
  - Queries: O(1) to O(log n) depending on query type

- **Session Storage**: O(1) for save/restore
  - Memory-efficient with JSON serialization
  - Disk persistence optional

## Troubleshooting

### Issue: Files not being detected

**Solution:** Check that directories aren't in the ignore list:
```python
# Modify scan to include specific directories
dirs[:] = [d for d in dirs if d not in ['__pycache__']]
```

### Issue: Slow repository scans

**Solution:** Use incremental scanning:
```python
# Only scan changed files
changed_files = [f for f in files if db.files[f].checksum != new_checksum]
```

### Issue: Knowledge graph too large

**Solution:** Prune low-value connections:
```python
# Remove edges with low weight
db.knowledge_graph = {
    k: v for k, v in db.knowledge_graph.items() 
    if len(v) > 1  # Keep only multi-connected nodes
}
```

## Examples

### Complete Workflow Example

```python
from workflow_database import WorkflowDatabase, WorkflowDefinition, initialize_default_workflows

# Initialize
db = WorkflowDatabase()

# Scan and setup
stats = db.scan_repository()
initialize_default_workflows(db)
db.build_knowledge_graph()

# Get workflow
workflow = db.workflows['ui_generation']

# Execute steps
for step in workflow.steps:
    print(f"Step {step['step']}: {step['action']}")
    # Execute with agent system
    agent_name = step['agent']
    # result = agents[agent_name].execute(...)

# Generate report
print(db.generate_report())

# Export for backup
db.export_database("workflow_backup.json")
```

## Future Enhancements

- [ ] Workflow visualization graphs
- [ ] Real-time workflow execution monitoring
- [ ] Automatic workflow optimization
- [ ] Machine learning for success prediction
- [ ] Distributed workflow execution
- [ ] Version control integration
- [ ] Collaborative multi-user workflows

## See Also

- [Enhanced NLP System](ENHANCED_NLP.md)
- [Enhanced Web System](ENHANCED_WEB.md)
- [Comprehensive Integration](COMPREHENSIVE_INTEGRATION.md)
- [Context Engine](CONTEXT_ENGINE.md)
- [Agent System](AGENT_INTEGRATION.md)
