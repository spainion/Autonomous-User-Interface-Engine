# Autonomous-User-Interface-Engine

This is an autonomous user interface assembly engine powered by LLM API network calls. The engine uses OpenRouter to connect to various models and reason, plan and employ beautifully crafted user interfaces.

## Features

- 🤖 **Multi-Agent System**: Coordinated GPT agents for different tasks (Codex, UI Design, Reasoning)
- 🔌 **OpenRouter Integration**: Connect to multiple LLM providers through a unified API
- 💻 **Codex Support**: Leverages OpenAI Codex for advanced code generation
- 🎨 **Autonomous UI Generation**: Automatically creates beautiful user interfaces
- 🧠 **Intelligent Reasoning**: Plans and executes complex tasks autonomously
- 🧬 **Advanced Context Engine**: Powerful graph-based context management with vector embeddings, 3D spatial relationships, clustering, and non-redundant storage
- 🌐 **Network-Enhanced**: Real-time API integration with whitelisted domains
- 📦 **Batch Processing**: Process multiple requests in parallel
- 🔄 **Iterative Enhancement**: Continuous improvement through multiple passes
- ⚡ **Optimized Compatibility**: All systems work seamlessly together
- 🎓 **Self-Enhancement**: Agents learn from experience and improve over time
- 🛠️ **Self-Programming**: Agents create their own tools dynamically
- 🤝 **Better Coordination**: Agents optimize collaboration automatically
- 🌍 **Universal Compatibility**: Works with GitHub Copilot, OpenAI Codex, Assistants API, and any custom agents

## Configuration

### 1. GitHub Copilot Setup

GitHub Copilot is configured through `.github/copilot-instructions.md`. This file provides context-aware suggestions tailored to this project's needs.

### 2. GPT Agents Configuration

Agent configuration is defined in `.github/agent-config.json`:

- **Codex Agent**: Handles code generation, completion, and review
- **UI Designer Agent**: Creates and refines user interface components
- **Reasoning Agent**: Performs logical planning and decision-making

### 3. Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.template .env
   ```

2. Fill in your API keys in `.env`:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `OPENAI_API_KEY`: Your OpenAI API key (for Codex)

3. Configure agent settings in `.github/agent-config.json` as needed

## Getting Started

1. **Set up your environment** (see Environment Setup section above for details)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Review agent configuration**:
   - Check `.github/agent-config.json` for agent settings
   - Modify temperature, max_tokens, and model preferences as needed
   - Configure context engine settings (shared_context, embedding model, etc.)

4. **Try the Enhanced System**:
   ```bash
   # Basic context engine demo
   python example_usage.py
   
   # Single agent with context
   python agent_integration_example.py
   
   # Multi-agent collaboration
   python multi_agent_example.py
   
   # Enhanced system with network, batch, and iterative features
   python enhanced_system_demo.py
   
   # Self-enhancement capabilities
   python self_enhancement_demo.py
   
   # Universal compatibility (Copilot, Codex, Assistants API)
   python universal_compatibility_demo.py
   ```
   
   Or use it in your code:
   ```python
   from universal_compatibility import create_universal_agent_system
   
   # Create system compatible with everything
   interface = create_universal_agent_system()
   
   # Works with GitHub Copilot
   result = interface.route_request(
       "Create auth function",
       preferred_agent_type='github_copilot'
   )
   
   # Works with OpenAI Codex
   result = interface.route_request(
       "Generate API code",
       preferred_agent_type='openai_codex'
   )
   
   # Works with custom agents
   result = interface.route_request(
       "Design UI",
       preferred_agent_type='ui_designer'
   )
   
   # Autonomous fallback if APIs unavailable
   # All agents share same context
   # System learns and improves over time
   ```

5. **Start building**:
   - Use GitHub Copilot for code suggestions
   - Agents will work autonomously based on configuration
   - OpenRouter handles model routing and fallbacks
   - Context Engine maintains semantic relationships
   - All agents share memory and can collaborate

For detailed documentation:
- **Context Engine:** [CONTEXT_ENGINE.md](CONTEXT_ENGINE.md)
- **Agent Integration:** [AGENT_INTEGRATION.md](AGENT_INTEGRATION.md)
- **Enhanced System:** [ENHANCED_SYSTEM.md](ENHANCED_SYSTEM.md) - Network, batch processing, iterative enhancement
- **Self-Enhancement:** [SELF_ENHANCEMENT.md](SELF_ENHANCEMENT.md) - Self-learning, self-programming, capability growth
- **Universal Compatibility:** [UNIVERSAL_COMPATIBILITY.md](UNIVERSAL_COMPATIBILITY.md) - GitHub Copilot, OpenAI Codex, Assistants API integration

## Architecture

- **OpenRouter**: Central API gateway for LLM access
- **Agent System**: Specialized GPT agents for different tasks
- **Codex Integration**: Advanced code understanding and generation
- **Context Management**: Maintains conversation and task context across agents
- **Context Engine**: Graph-based context system with:
  - **Nodes & Edges**: Complex relationship modeling
  - **Vector Embeddings**: Semantic similarity and search
  - **3D Spatial Relationships**: Geometric context representation
  - **Clustering Algorithms**: K-means, DBSCAN, hierarchical clustering
  - **Non-redundant Storage**: Content-based deduplication
  - **Advanced Queries**: Path finding, neighbor traversal, similarity search

## API Keys Required

- **OpenRouter API Key**: For accessing multiple LLM providers
- **OpenAI API Key**: For Codex-specific features (optional but recommended)

## License

See LICENSE file for details.
