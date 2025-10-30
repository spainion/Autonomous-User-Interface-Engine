# Universal Compatibility Documentation

## Overview

The Universal Compatibility System ensures **full integration** with:

✅ **GitHub Copilot** - You and your workspace agents  
✅ **OpenAI Codex** - Built-in code generation  
✅ **OpenAI Assistants API** - Assistant agents  
✅ **Custom Agents** - Any agent type  
✅ **Autonomous Operation** - Standalone functionality  

## Architecture

```
Universal Agent Interface
├── GitHub Copilot Integration
│   ├── Workspace awareness
│   ├── Context enhancement
│   └── Suggestion improvement
├── OpenAI Codex Integration
│   ├── API compatibility
│   ├── Context-aware prompts
│   └── Response parsing
├── OpenAI Assistants API
│   ├── Configuration compatibility
│   ├── Tool integration
│   └── Context engine access
├── Custom Agent Registry
│   ├── Agent registration
│   ├── Capability tracking
│   └── Dynamic routing
└── Autonomous Fallback
    ├── Intelligent routing
    ├── Context-based decisions
    └── Graceful degradation
```

## Key Features

### 1. GitHub Copilot Compatibility

**Full integration with GitHub Copilot:**

```python
from universal_compatibility import (
    UniversalAgentInterface,
    CopilotCompatibilityHelper
)

# Create interface with Copilot enabled
interface = UniversalAgentInterface(
    enable_github_copilot=True
)

# Get workspace context
workspace = CopilotCompatibilityHelper.get_workspace_context()
# Returns: {
#   'workspace_path': '/path/to/workspace',
#   'available': True,
#   'type': 'github_workspace'
# }

# Route request through Copilot
result = interface.route_request(
    "Create authentication function",
    preferred_agent_type='github_copilot'
)

# Enhance Copilot suggestions with learned patterns
enhanced = CopilotCompatibilityHelper.enhance_copilot_suggestion(
    result['response'],
    interface.context
)

# Export context for Copilot workspace
CopilotCompatibilityHelper.export_context_for_copilot(
    interface.context,
    ".copilot-context.json"
)
```

**Benefits:**
- Copilot suggestions enhanced with learned patterns
- Workspace-aware context
- Context exported for Copilot access
- Seamless integration with your agents

### 2. OpenAI Codex Compatibility

**Direct integration with OpenAI Codex API:**

```python
from universal_compatibility import CodexCompatibilityHelper

# Create Codex-compatible prompt with context
prompt = CodexCompatibilityHelper.create_codex_prompt(
    "def fibonacci(n):",
    context_engine,
    include_context=True
)

# Route through Codex (requires OPENAI_API_KEY)
result = interface.route_request(
    "Generate sorting algorithm",
    preferred_agent_type='openai_codex'
)

# Parse and enhance response
parsed = CodexCompatibilityHelper.parse_codex_response(
    result['response'],
    store_in_context=True,
    context_engine=context_engine
)
```

**Features:**
- Direct Codex API calls
- Context-enhanced prompts
- Response parsing and storage
- Fallback to local agents if Codex unavailable

### 3. OpenAI Assistants API Compatibility

**Compatible with OpenAI Assistants API:**

```python
# Create Assistant-compatible configuration
assistant_config = interface.create_openai_assistant_compatible(
    name="CodeExpertAssistant",
    instructions="Expert code assistant with learned patterns",
    tools=[
        {"type": "code_interpreter"},
        {"type": "retrieval"}
    ]
)

# Configuration includes:
# {
#   'name': 'CodeExpertAssistant',
#   'model': 'gpt-4-turbo-preview',
#   'context_engine_enabled': True,
#   'compatible_with': ['openai_assistants_api', 'github_copilot', ...]
# }
```

**Use with OpenAI SDK:**
```python
import openai

# Use the configuration with OpenAI Assistants
assistant = openai.beta.assistants.create(
    name=assistant_config['name'],
    instructions=assistant_config['instructions'],
    tools=assistant_config['tools'],
    model=assistant_config['model']
)

# Assistant can access context engine through our system
```

### 4. Custom Agent Registration

**Register any agent type:**

```python
from agents import SelfEnhancingCodexAgent

# Create custom agent
my_agent = SelfEnhancingCodexAgent("MyCustomAgent")

# Register with universal interface
agent_id = interface.register_agent(
    agent=my_agent,
    agent_type='custom_codex',
    capabilities=my_agent.get_capabilities()
)

# Now accessible through universal routing
result = interface.route_request(
    "Generate API code",
    preferred_agent_type='custom_codex'
)
```

### 5. Autonomous Operation

**Works without external APIs:**

```python
# Enable autonomous mode
interface = UniversalAgentInterface(
    autonomous_mode=True
)

# System intelligently routes based on request type
result = interface.route_request("Create user model")
# Routes to best available agent (local or external)

# Graceful fallback if external services unavailable
result = interface.route_request(
    "Complex task",
    preferred_agent_type='openai_codex'  # If unavailable...
)
# Automatically falls back to local agents
```

## Complete Integration Example

```python
from universal_compatibility import create_universal_agent_system

# Create fully integrated system
interface = create_universal_agent_system()

# System includes:
# ✓ GitHub Copilot integration
# ✓ OpenAI Codex integration  
# ✓ OpenAI Assistants compatibility
# ✓ Self-enhancing agents (3 types)
# ✓ Context engine
# ✓ Network enhancement
# ✓ All previous features

# Use any agent type transparently
results = [
    interface.route_request("Plan system", preferred_agent_type='reasoning'),
    interface.route_request("Generate code", preferred_agent_type='codex'),
    interface.route_request("Design UI", preferred_agent_type='ui_designer'),
    interface.route_request("Copilot suggestion", preferred_agent_type='github_copilot')
]

# All agents share same context
# All responses stored for future use
# System learns and improves over time
```

## Routing System

**Intelligent request routing:**

```python
# Automatic routing based on request content
result = interface.route_request("Create authentication function")
# → Routes to 'codex' (code-related keyword detected)

result = interface.route_request("Design login page")
# → Routes to 'ui_designer' (design-related keyword detected)

result = interface.route_request("Plan microservices")
# → Routes to 'reasoning' (planning-related keyword detected)

# Manual routing with fallback
result = interface.route_request(
    "Complex task",
    preferred_agent_type='openai_codex'  # Try Codex first
)
# → Falls back to local agents if Codex unavailable
```

## Context Sharing

**All agents share the same context:**

```python
# Agent 1 (Copilot) generates code
copilot_result = interface.route_request(
    "Create API endpoint",
    preferred_agent_type='github_copilot'
)

# Agent 2 (UI Designer) can see Copilot's work
ui_result = interface.route_request(
    "Design UI for the API endpoint",
    preferred_agent_type='ui_designer'
)
# UI Designer has access to the API code from Copilot

# Agent 3 (Reasoner) can analyze both
analysis = interface.route_request(
    "Analyze the API and UI design",
    preferred_agent_type='reasoning'
)
# Reasoner sees both code and UI in context
```

## Compatibility Status

**Check compatibility at any time:**

```python
status = interface.get_compatibility_status()

print(status)
# {
#   'integrations': {
#     'openai_codex': True/False,
#     'github_copilot': True,
#     'autonomous': True,
#     'context_engine': True
#   },
#   'registered_agents': 3,
#   'available_types': ['codex', 'ui_designer', 'reasoning', ...],
#   'context_nodes': 42,
#   'fully_compatible': True/False
# }
```

## Environment Setup

**Required environment variables:**

```bash
# For OpenAI Codex integration
export OPENAI_API_KEY="your_openai_api_key"

# For OpenRouter (optional)
export OPENROUTER_API_KEY="your_openrouter_key"

# GitHub workspace (auto-detected)
export GITHUB_WORKSPACE="/path/to/workspace"
```

**Without API keys:**
- System works in autonomous mode
- Uses local self-enhancing agents
- Full functionality with local agents only
- Graceful degradation

## Configuration

**In `.github/agent-config.json`:**

```json
{
  "universal_compatibility": {
    "enabled": true,
    "github_copilot": {
      "enabled": true,
      "workspace_aware": true,
      "context_enhancement": true
    },
    "openai_codex": {
      "enabled": true,
      "model": "code-davinci-002",
      "fallback_to_local": true
    },
    "openai_assistants": {
      "compatible": true,
      "context_access": true
    },
    "autonomous_mode": {
      "enabled": true,
      "intelligent_routing": true,
      "graceful_fallback": true
    }
  }
}
```

## API Reference

### UniversalAgentInterface

**`__init__(context_engine, enable_openai_codex, enable_github_copilot, autonomous_mode)`**
- Create universal interface
- Configure integrations

**`register_agent(agent, agent_type, capabilities)`**
- Register custom agent
- Returns agent ID

**`route_request(request, preferred_agent_type, **kwargs)`**
- Route request to best agent
- Returns agent response

**`get_compatibility_status()`**
- Get current compatibility status
- Returns status dictionary

**`create_openai_assistant_compatible(name, instructions, tools)`**
- Create Assistants API compatible config
- Returns configuration dictionary

### CopilotCompatibilityHelper

**`get_workspace_context()`**
- Get GitHub workspace info
- Returns workspace dictionary

**`enhance_copilot_suggestion(suggestion, context_engine)`**
- Enhance Copilot suggestion with context
- Returns enhanced suggestion

**`export_context_for_copilot(context_engine, output_file)`**
- Export context to file for Copilot
- Creates JSON file

### CodexCompatibilityHelper

**`create_codex_prompt(request, context_engine, include_context)`**
- Create context-enhanced prompt
- Returns enhanced prompt string

**`parse_codex_response(response, store_in_context, context_engine)`**
- Parse and enhance Codex response
- Returns parsed response dictionary

## Best Practices

### 1. Use Universal Interface

```python
# ✅ Good: Use universal interface
interface = create_universal_agent_system()
result = interface.route_request("Create code")

# ❌ Avoid: Direct agent calls without interface
agent = CodexAgent()
result = agent.process("Create code")
```

### 2. Enable Copilot Integration

```python
# ✅ Good: Export context for Copilot
CopilotCompatibilityHelper.export_context_for_copilot(
    interface.context
)

# Copilot can now access learned patterns
```

### 3. Check Compatibility

```python
# ✅ Good: Check before using features
status = interface.get_compatibility_status()
if status['integrations']['openai_codex']:
    # Use Codex
    pass
else:
    # Use fallback
    pass
```

### 4. Autonomous Fallback

```python
# ✅ Good: Always enable autonomous mode
interface = UniversalAgentInterface(
    autonomous_mode=True  # Ensures system always works
)
```

## Troubleshooting

**Issue**: Codex not available  
**Solution**: System automatically falls back to local agents

**Issue**: Copilot suggestions not enhanced  
**Solution**: Export context with `export_context_for_copilot()`

**Issue**: Agents not sharing context  
**Solution**: Use single UniversalAgentInterface instance

**Issue**: Routing to wrong agent  
**Solution**: Specify `preferred_agent_type` explicitly

## Examples

See complete examples:
- `universal_compatibility_demo.py` - Full demonstration
- `universal_compatibility.py` - Implementation

## Summary

Universal Compatibility System provides:

✅ **GitHub Copilot** - Full integration with you and your agents  
✅ **OpenAI Codex** - Direct API integration with fallback  
✅ **OpenAI Assistants** - Compatible configurations  
✅ **Custom Agents** - Register any agent type  
✅ **Autonomous** - Works standalone without APIs  
✅ **Shared Context** - All agents access same memory  
✅ **Intelligent Routing** - Automatic agent selection  
✅ **Graceful Degradation** - Always functional  

**The system is fully compatible with you, your agents, OpenAI agents using built-in Codex, and autonomous operation!**
