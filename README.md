# Autonomous-User-Interface-Engine

This is an autonomous user interface assembly engine powered by LLM API network calls. The engine uses OpenRouter to connect to various models and reason, plan and employ beautifully crafted user interfaces.

## Features

- 🤖 **Multi-Agent System**: Coordinated GPT agents for different tasks (Codex, UI Design, Reasoning)
- 🔌 **OpenRouter Integration**: Connect to multiple LLM providers through a unified API
- 💻 **Codex Support**: Leverages OpenAI Codex for advanced code generation
- 🎨 **Autonomous UI Generation**: Automatically creates beautiful user interfaces
- 🧠 **Intelligent Reasoning**: Plans and executes complex tasks autonomously
- 🧬 **Advanced Context Engine**: Powerful graph-based context management with vector embeddings, 3D spatial relationships, clustering, and non-redundant storage

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

4. **Try the Context Engine**:
   ```bash
   # Basic context engine demo
   python example_usage.py
   
   # Single agent with context
   python agent_integration_example.py
   
   # Multi-agent collaboration
   python multi_agent_example.py
   ```
   
   Or use it in your code:
   ```python
   from context_engine import ContextEngine
   from agents import CodexAgent, UIDesignerAgent, ReasoningAgent
   
   # Use context engine directly
   engine = ContextEngine()
   node = engine.add_node(content="Your content here", node_type="knowledge")
   similar = engine.find_similar_nodes(query_embedding, k=5)
   
   # Or use context-aware agents
   codex = CodexAgent("MyCodeBot")
   result = codex.process_request("Generate authentication API")
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
