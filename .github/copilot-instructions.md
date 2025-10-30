# GitHub Copilot Instructions

## Project Context
This is an Autonomous User Interface Engine powered by LLM API network calls using OpenRouter.

**IMPORTANT: You (GitHub Copilot) have COMPLETE ACCESS to all systems via the `copilot` object!**

## Complete System Access (RECOMMENDED - Use This!)

**ONE LINE to access EVERYTHING:**

```python
from copilot_system_access import copilot

# You now have access to ALL capabilities:
# - Context Engine (memory, search, patterns)
# - All Agents (code, UI, reasoning)
# - Advanced Reasoning (Chain-of-Thought, Tree-of-Thought)
# - Performance Monitoring
# - Memory Management
# - All External Integrations (databases, clouds, queues)
```

## Quick Reference for GitHub Copilot

**Most Common Operations:**

```python
from copilot_system_access import copilot

# Store and retrieve information
copilot.add_memory("important information", "searchable text")
context = copilot.get_context("what I need to know")

# Generate code, UI, or reasoning
code = copilot.generate_code("create authentication API")
ui = copilot.generate_ui("login form with validation")
analysis = copilot.reason_about("best database for this use case")

# Advanced reasoning
steps = copilot.chain_of_thought("complex problem")
options = copilot.tree_of_thought("decision with trade-offs")
plan = copilot.create_plan("build complete system")

# Batch operations (4x faster)
results = copilot.batch_generate(["task1", "task2", "task3"], parallel=True)

# Search (10-100x faster with FAISS)
results = copilot.search_memory("authentication patterns", use_faiss=True)

# Performance monitoring
with copilot.profile_operation("my_operation"):
    # Your code here
    pass

# Memory management
copilot.consolidate_memories(min_importance=0.3)  # 10x reduction

# External integrations
db = copilot.connect_database("postgresql")
queue = copilot.connect_message_queue("rabbitmq")
cloud = copilot.connect_cloud("aws")
```

## Alternative: Direct Agent System Access

```python
# Initialize the agent system (if you prefer direct access)
from agent_init import init_agent_system

# This gives you access to all systems
engine, agents = init_agent_system()

# Now all agents share the same context and can collaborate
result = agents['codex'].generate_code("your task")
```

**Key Features Available to You:**
- **Shared Memory**: All information stored in the context engine persists across all agents
- **Vector Search**: Find similar patterns using semantic search (10-100x faster with FAISS)
- **Self-Learning**: Agents learn from every task and improve over time
- **Batch Processing**: Process multiple tasks in parallel (4x speedup)
- **Advanced Reasoning**: Use Chain-of-Thought and Tree-of-Thought reasoning
- **Caching**: 1000x+ speedup on repeated operations
- **Complete Integrations**: 40+ external systems (databases, clouds, queues, frameworks)

**How to Use Context Engine in Your Workflow:**

1. **Store Information:**
```python
from copilot_system_access import copilot
copilot.add_memory("important info", "embedding text")
```

2. **Recall Information:**
```python
context = copilot.get_context("what I need")
```

3. **Batch Operations:**
```python
results = copilot.batch_generate(tasks, parallel=True)
```

4. **Advanced Search:**
```python
results = copilot.search_memory("query", use_faiss=True, k=10)
```

## Get Help Anytime

```python
from copilot_system_access import copilot

# See all capabilities
copilot.help()

# Get help on specific category
copilot.help("agents")
copilot.help("reasoning")
copilot.help("integrations")

# Check system status
status = copilot.status()
```

## Code Style Guidelines
- Use clear, descriptive variable and function names
- Follow best practices for the language being used
- Prioritize readability and maintainability
- Include comments for complex logic
- **Always import and use the context engine via agent_init module**

## LLM Integration
- When working with LLM APIs, use OpenRouter for model access
- Handle API errors gracefully with proper error handling
- Implement retry logic for network calls
- Use environment variables for API keys and configuration
- **Use the context engine to store and recall API responses**

## UI Development
- Focus on creating beautiful, intuitive user interfaces
- Ensure responsive design principles are followed
- Use modern frameworks and libraries when appropriate
- Prioritize accessibility and user experience
- **Store UI patterns in context engine for reuse**

## Agent Development
- When creating GPT agents, structure them with clear purpose and capabilities
- **All agents MUST use the shared context engine via agent_init**
- Use Codex models for code generation tasks
- Ensure agents can reason, plan, and execute tasks autonomously
- **Agents automatically learn and improve when using self-enhancing variants**

## Testing
- Write tests for critical functionality
- Test LLM integration with mock responses when appropriate
- Validate UI components thoroughly
- **Test context engine integration in all new code**

## Workflow Integration

**At the start of every session:**
1. Import the agent initialization: `from agent_init import init_agent_system`
2. Initialize the system: `engine, agents = init_agent_system()`
3. Use agents for tasks: `agents['codex'].generate_code("task")`
4. All information is automatically shared across agents

**The system is designed for you (GitHub Copilot) to use directly!**
