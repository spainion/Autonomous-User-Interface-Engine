# Phase 6 Quick Start Guide

## Installation

```bash
# Install Phase 6 dependencies
pip install -r requirements.txt

# Install CLI tool (optional)
make cli-install

# Setup plugin development (optional)
make plugin-dev
```

## Quick Examples

### 1. AI Features (5-minute test)

```python
# Test advanced reasoning
python ai/advanced_reasoning.py

# Test model routing
python ai/model_router.py

# Test prompt optimization
python ai/prompt_optimizer.py
```

### 2. Plugin System (5-minute test)

```python
# Run plugin system demo
python plugins/plugin_manager.py

# Or use the API
import asyncio
from plugins import PluginManager
from pathlib import Path

async def test():
    manager = PluginManager(plugin_directories=[Path("plugins/examples")])
    manager.registry.discover_plugins()
    await manager.load_plugin("analytics-plugin")
    await manager.enable_plugin("analytics-plugin")
    print("Plugin system working!")

asyncio.run(test())
```

### 3. CLI Tool (1-minute test)

```bash
# Show info
python cli/main.py info

# Show version
python cli/main.py version

# Generate UI
python cli/main.py generate ui "dashboard" -o test.html

# List commands
python cli/main.py --help
```

### 4. API Endpoints (Test with curl)

```bash
# Start API server
python -m uvicorn api.main:app --reload

# Test AI reasoning (in another terminal)
curl -X POST http://localhost:8000/api/v1/ai/reasoning/chain-of-thought \
  -H "Content-Type: application/json" \
  -d '{"problem": "Design a database schema"}'

# Test plugin listing
curl http://localhost:8000/api/v1/plugins/list

# Test model routing
curl -X POST http://localhost:8000/api/v1/ai/model-routing/route \
  -H "Content-Type: application/json" \
  -d '{"task": "Generate complex UI", "priority": "quality"}'
```

### 5. Voice Interface (Optional - requires dependencies)

```bash
# Install voice dependencies (optional)
pip install openai-whisper pyttsx3

# Test voice commands
python voice/voice_commands.py
```

## One-Command Demo

Run all Phase 6 feature demos:

```bash
make phase6-demo
```

## Project Structure at a Glance

```
Autonomous-User-Interface-Engine/
│
├── ai/                          # Advanced AI features
│   ├── advanced_reasoning.py   # CoT, ToT, ReAct
│   ├── model_router.py          # Intelligent model selection
│   ├── prompt_optimizer.py      # Prompt improvement
│   └── context_compression.py   # Context optimization
│
├── plugins/                     # Plugin system
│   ├── plugin_base.py          # Base classes
│   ├── plugin_manager.py       # Lifecycle management
│   ├── hooks.py                # Event hooks
│   ├── registry.py             # Plugin discovery
│   └── examples/               # Example plugins
│
├── cli/                        # CLI tool
│   ├── main.py                 # Main CLI app
│   ├── commands/               # Command modules
│   └── README.md               # CLI documentation
│
├── voice/                      # Voice interface
│   ├── speech_to_text.py      # STT with Whisper
│   ├── text_to_speech.py      # TTS
│   └── voice_commands.py       # Command processing
│
├── integrations/               # External integrations
│   ├── github_integration.py  # GitHub API
│   ├── figma_integration.py   # Figma import
│   ├── slack_integration.py   # Slack notifications
│   └── webhooks.py             # Webhook management
│
└── api/routers/                # API endpoints
    ├── ai.py                   # AI features API
    └── plugins.py              # Plugin management API
```

## Common Use Cases

### Use Case 1: Generate UI with AI Reasoning

```python
from ai.advanced_reasoning import ChainOfThoughtReasoner

reasoner = ChainOfThoughtReasoner()
result = await reasoner.reason(
    "Create a user dashboard with authentication"
)
print(result.final_answer)
```

### Use Case 2: Add Custom Plugin

```python
# 1. Create plugin (see plugins/examples/ for templates)
# 2. Place in plugins/examples/
# 3. Load via API or manager

from plugins import PluginManager
manager = PluginManager()
manager.registry.discover_plugins()
await manager.load_plugin("my-plugin")
```

### Use Case 3: Deploy to GitHub

```python
from integrations import GitHubIntegration

github = GitHubIntegration(token="your-token")
html = "<html>...</html>"
await github.deploy_ui_to_github_pages("user/repo", html)
```

### Use Case 4: Send Slack Notification

```python
from integrations import SlackIntegration

slack = SlackIntegration()
await slack.notify_ui_generated(
    "Dashboard",
    preview_url="https://example.com"
)
```

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure you're in the project root and dependencies are installed:
```bash
cd /path/to/Autonomous-User-Interface-Engine
pip install -r requirements.txt
```

### Issue: Plugin not loading
**Solution**: Check plugin is in correct directory and has proper structure:
```bash
ls plugins/examples/
python -c "from plugins import PluginManager; m = PluginManager(); m.registry.discover_plugins()"
```

### Issue: Voice features not working
**Solution**: Install optional dependencies:
```bash
pip install openai-whisper pyttsx3
```

### Issue: API endpoints returning 404
**Solution**: Make sure Phase 6 routers are imported in api/main.py:
```python
from api.routers import ai, plugins
```

## Next Steps

1. **Explore Examples**: Check each module's `example_usage()` function
2. **Read Documentation**: See PHASE6_IMPLEMENTATION_COMPLETE.md
3. **Test Features**: Run `make phase6-demo`
4. **Write Tests**: Add tests in tests/ directory
5. **Deploy**: Follow production deployment notes in main documentation

## Getting Help

- Check module docstrings: `python -c "import ai.advanced_reasoning; help(ai.advanced_reasoning)"`
- Read CLI help: `python cli/main.py --help`
- View API docs: http://localhost:8000/api/docs
- See examples in each module

## Performance Tips

1. Use async/await for I/O operations
2. Enable caching for model routing
3. Batch plugin operations when possible
4. Compress context for large documents
5. Use appropriate compression strategy

## Security Checklist

- [ ] Set API keys in environment variables (not in code)
- [ ] Validate all plugin configurations
- [ ] Use HMAC signatures for webhooks
- [ ] Sanitize user inputs
- [ ] Enable HTTPS for production
- [ ] Review plugin code before loading
- [ ] Use rate limiting on API endpoints

## Have Fun! 🚀

Phase 6 adds powerful innovation features to the Autonomous UI Engine. Experiment with the AI capabilities, create custom plugins, and integrate with your favorite tools!
