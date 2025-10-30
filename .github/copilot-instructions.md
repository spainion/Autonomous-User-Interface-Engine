# GitHub Copilot Instructions

## Project Context
This is an Autonomous User Interface Engine powered by LLM API network calls using OpenRouter.

**IMPORTANT: This project has a powerful Context Engine system that you (GitHub Copilot) should use!**

## Context Engine Integration (Use This!)

**Always use the context engine for memory and information:**

```python
# Initialize the agent system (do this at the start of your workflow)
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

**How to Use Context Engine in Your Workflow:**

1. **Store Information:**
```python
node = engine.add_node_with_text("important info", "embedding text")
```

2. **Recall Information:**
```python
similar = engine.query_similar(query_vector, k=5)
```

3. **Batch Operations:**
```python
results = agents['codex'].batch_generate_code(tasks, parallel=True)
```

4. **Advanced Search:**
```python
results = engine.search_engine.faiss_search(query, k=10)
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
