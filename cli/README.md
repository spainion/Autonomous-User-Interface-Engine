# Autonomous UI Engine CLI

Command-line interface for the Autonomous UI Engine with Rich formatting and Typer framework.

## Installation

```bash
pip install typer rich
python cli/main.py --install-completion
```

## Usage

### Basic Commands

```bash
# Show version
ui-engine version

# Show system status
ui-engine status

# Show system information
ui-engine info
```

### UI Generation

```bash
# Generate a UI from description
ui-engine generate ui "dashboard with charts" -o dashboard.html

# Generate with specific framework
ui-engine generate ui "login form" --framework react

# Generate a component
ui-engine generate component Button --props '{"variant":"primary"}'

# Generate a theme
ui-engine generate theme dark --colors '{"primary":"#007bff"}'
```

### Agent Management

```bash
# List all agents
ui-engine agents list

# Execute an agent
ui-engine agents execute "UI Generator" "create a landing page"

# Check agent status
ui-engine agents status "UI Generator"
```

### Context Operations

```bash
# Add to context
ui-engine context add "User prefers dark themes" --importance 0.8

# Search context
ui-engine context search "dark theme" --limit 5

# Show context statistics
ui-engine context stats

# Clear context (with confirmation)
ui-engine context clear
```

### Plugin Management

```bash
# List installed plugins
ui-engine plugins list

# Enable a plugin
ui-engine plugins enable analytics-plugin

# Disable a plugin
ui-engine plugins disable analytics-plugin

# Show plugin info
ui-engine plugins info analytics-plugin

# Install new plugin
ui-engine plugins install /path/to/plugin.py
```

### Configuration

```bash
# Show all configuration
ui-engine config show

# Set a configuration value
ui-engine config set llm.model gpt-4-turbo

# Get a configuration value
ui-engine config get llm.model

# Reset to defaults
ui-engine config reset --yes
```

## Command Groups

- **generate**: UI generation commands
- **agents**: Agent management
- **context**: Context database operations
- **plugins**: Plugin system management
- **config**: Configuration management

## Features

- ✨ Beautiful terminal UI with Rich
- 🎯 Type-safe commands with Typer
- 📊 Progress indicators and spinners
- 🎨 Syntax highlighting for code
- 📋 Formatted tables for data display
- ✅ Interactive confirmations
- 🔧 Auto-completion support

## Development

To add new commands:

1. Create a new file in `cli/commands/`
2. Define command functions with `@app.command()` decorator
3. Add the command group to `cli/main.py`

Example:

```python
# cli/commands/mycommand.py
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str):
    """Say hello."""
    console.print(f"Hello, [bold]{name}[/bold]!")
```

Then in `cli/main.py`:

```python
from cli.commands import mycommand
app.add_typer(mycommand.app, name="mycommand")
```

## Help

Get help for any command:

```bash
ui-engine --help
ui-engine generate --help
ui-engine agents execute --help
```
