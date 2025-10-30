# Agent Integration with Context Engine

## Overview

All agents in the Autonomous User Interface Engine are now integrated with the **Context Engine**, providing them with:
- **Shared memory** across all agents
- **Semantic recall** of past interactions
- **Pattern storage** and reuse
- **Agent collaboration** capabilities
- **Context-aware responses**

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Shared Context Engine                     │
│  (Graph + Vector Space + 3D Spatial + Clustering)           │
└─────────────────────────────────────────────────────────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────┐
    │  Codex   │     │    UI    │    │Reasoning │
    │  Agent   │◄───►│ Designer │◄──►│  Agent   │
    └──────────┘     └──────────┘    └──────────┘
         │                 │               │
         └─────────────────┴───────────────┘
              Agents collaborate via
              shared context and edges
```

## Agent Base Class

All agents inherit from `BaseAgent` which provides:

### Core Methods

#### `add_to_context(content, content_type, embedding, metadata)`
Store information in the shared context.

```python
node = agent.add_to_context(
    content="User requested login feature",
    content_type="user_request",
    embedding=embedding_vector,
    metadata={'priority': 'high'}
)
```

#### `recall_context(query_embedding, k, content_type)`
Retrieve relevant context based on semantic similarity.

```python
similar = agent.recall_context(
    query_embedding=embedding,
    k=5,
    content_type="code_pattern"
)
```

#### `share_with_agent(target_agent_name, content, relationship_type)`
Share information with another agent.

```python
codex_agent.share_with_agent(
    "UIDesignerAgent",
    {"api": "authentication"},
    "backend_api"
)
```

#### `collaborate_with(other_agent_name)`
Establish a collaboration relationship.

```python
reasoning_agent.collaborate_with("CodexAgent")
```

#### `get_agent_history()`
Get all items created by this agent.

```python
history = agent.get_agent_history()
for item in history:
    print(f"Created: {item.content}")
```

## Implemented Agents

### 1. CodexAgent
**Type:** `codex`  
**Capabilities:**
- Code generation
- Code completion
- Code review
- Refactoring
- Bug detection

**Usage:**
```python
from agents import CodexAgent

codex = CodexAgent("CodeBot")
result = codex.process_request(
    "Generate user authentication API",
    language="python"
)
print(result['code'])
```

**Context Storage:**
- Stores generated code with embeddings
- Recalls similar code patterns
- Shares code with UI agents

### 2. UIDesignerAgent
**Type:** `ui_designer`  
**Capabilities:**
- UI design
- Component generation
- Layout planning
- Accessibility review
- Responsive design

**Usage:**
```python
from agents import UIDesignerAgent

ui = UIDesignerAgent("DesignBot")
result = ui.process_request(
    "Create login form component",
    framework="react",
    style="modern"
)
print(result['ui_component'])
```

**Context Storage:**
- Stores UI designs with embeddings
- Recalls similar design patterns
- Shares components with code agents

### 3. ReasoningAgent
**Type:** `reasoning`  
**Capabilities:**
- Logical reasoning
- Planning
- Decision making
- Problem decomposition
- Strategy formation

**Usage:**
```python
from agents import ReasoningAgent

reasoner = ReasoningAgent("PlannerBot")
result = reasoner.process_request(
    "Plan a user authentication system",
    complexity="medium",
    domain="software_engineering"
)
print(result['reasoning']['plan'])
```

**Context Storage:**
- Stores reasoning chains
- Recalls similar problems
- Shares plans with execution agents

## Creating Custom Agents

To create your own context-aware agent:

```python
from agents import BaseAgent
from typing import List, Dict, Any

class MyCustomAgent(BaseAgent):
    def __init__(self, agent_name: str = "CustomAgent"):
        super().__init__(agent_name, agent_type="custom")
    
    def get_capabilities(self) -> List[str]:
        return [
            'capability_1',
            'capability_2',
            'capability_3'
        ]
    
    def process_request(self, request: str, **kwargs) -> Dict[str, Any]:
        # 1. Recall relevant context
        embedding = self._create_embedding(request)
        context = self.recall_context(embedding, k=5)
        
        # 2. Process with context
        result = self._do_work(request, context)
        
        # 3. Store in context
        self.add_to_context(
            content=result,
            content_type="my_result",
            embedding=embedding
        )
        
        return {'result': result}
```

## Multi-Agent Collaboration

Agents automatically share the same context engine:

```python
from agents import CodexAgent, UIDesignerAgent, ReasoningAgent

# All agents share context automatically
reasoner = ReasoningAgent("Planner")
coder = CodexAgent("Coder")
designer = UIDesignerAgent("Designer")

# Establish collaboration
reasoner.collaborate_with("Coder")
coder.collaborate_with("Designer")

# Agents can now see each other's work
plan = reasoner.process_request("Plan a feature")
reasoner.share_with_agent("Coder", plan['reasoning'], "task_plan")

# Coder can recall the plan
code = coder.process_request("Implement the planned feature")
```

## Configuration

In `.github/agent-config.json`:

```json
{
  "agents": {
    "codex": {
      "use_context_engine": true,
      "context_recall_limit": 5
    }
  },
  "context_engine": {
    "enabled": true,
    "shared_context": true,
    "embedding_backend": "openai",
    "embedding_model": "text-embedding-3-small",
    "features": {
      "deduplication": true,
      "vector_similarity": true,
      "spatial_queries": true,
      "clustering": true
    }
  }
}
```

## Context Features Available to Agents

### 1. Deduplication
Agents automatically avoid storing duplicate information.

### 2. Vector Similarity
Agents can find semantically similar past work.

### 3. Spatial Queries
Agents can find contextually nearby information in 3D space.

### 4. Clustering
Agents can cluster related information for better organization.

### 5. Path Finding
Agents can trace relationships and reasoning chains.

### 6. Temporal Tracking
Agents can see the sequence of events and decisions.

## Best Practices

### 1. Always Store Important Work
```python
result = agent.process_request("important task")
agent.add_to_context(
    result,
    content_type="important_result",
    metadata={'reviewed': True}
)
```

### 2. Recall Before Acting
```python
embedding = create_embedding(request)
past_similar = agent.recall_context(embedding, k=5)
# Use past_similar to inform current work
```

### 3. Share Across Agents
```python
# After completing work
agent.share_with_agent(
    "OtherAgent",
    result,
    "completion_of_task"
)
```

### 4. Establish Collaborations
```python
# At initialization
agent1.collaborate_with("Agent2")
agent2.collaborate_with("Agent3")
```

### 5. Store Reusable Patterns
```python
codex.store_code_pattern(
    "authentication_api",
    code,
    "Standard auth API pattern"
)
```

## Context Statistics

Monitor agent context usage:

```python
stats = agent.get_context_stats()
print(f"Items created: {stats['items_created']}")
print(f"Total context nodes: {stats['total_context_nodes']}")
print(f"Collaborators: {stats['collaborators']}")
```

## Examples

See these files for complete examples:
- `agent_integration_example.py` - Single agent with context
- `multi_agent_example.py` - Multiple agents collaborating

## Integration with Your Agent

To integrate the context engine with your existing agent:

1. **Inherit from BaseAgent:**
   ```python
   from agents import BaseAgent
   
   class YourAgent(BaseAgent):
       def __init__(self):
           super().__init__("YourAgentName", "your_type")
   ```

2. **Implement required methods:**
   ```python
   def get_capabilities(self) -> List[str]:
       return ['cap1', 'cap2']
   
   def process_request(self, request: str, **kwargs) -> Dict[str, Any]:
       # Your implementation
       pass
   ```

3. **Use context methods:**
   - `add_to_context()` - Store information
   - `recall_context()` - Retrieve similar information
   - `share_with_agent()` - Share with other agents

## Troubleshooting

**Issue:** Agent can't recall context  
**Solution:** Ensure embeddings are being generated and stored

**Issue:** Agents not collaborating  
**Solution:** Call `collaborate_with()` to establish relationships

**Issue:** Too much context  
**Solution:** Adjust `context_recall_limit` in agent config

**Issue:** Slow similarity search  
**Solution:** Reduce `k` parameter or use clustering

## Future Enhancements

- Persistent storage backends
- Context compression
- Advanced query languages
- Visual context graphs
- Real-time collaboration monitoring

## Summary

The Context Engine integration gives all agents:
✅ Shared memory across agents  
✅ Semantic understanding of past work  
✅ Collaboration capabilities  
✅ Pattern recognition and reuse  
✅ Context-aware decision making  

This creates a truly intelligent multi-agent system where agents learn from each other and build collective knowledge.
