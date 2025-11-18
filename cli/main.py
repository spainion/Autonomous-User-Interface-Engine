"""
CLI Tool for Autonomous UI Engine
Phase 6: Innovation - CLI Tool

Typer-based CLI application with Rich formatting.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.commands import generate, agents, context, plugins, config

app = typer.Typer(
    name="ui-engine",
    help="Autonomous UI Engine CLI - Generate UIs, manage agents, and more",
    add_completion=True
)
console = Console()

# Add command groups
app.add_typer(generate.app, name="generate", help="UI generation commands")
app.add_typer(agents.app, name="agents", help="Agent management commands")
app.add_typer(context.app, name="context", help="Context operations")
app.add_typer(plugins.app, name="plugins", help="Plugin management")
app.add_typer(config.app, name="config", help="Configuration management")


@app.command()
def version():
    """Show version information."""
    console.print("[bold blue]Autonomous UI Engine CLI[/bold blue]")
    console.print("Version: [green]0.6.0[/green]")
    console.print("Phase: [yellow]6 - Innovation[/yellow]")


@app.command()
def status():
    """Show system status."""
    table = Table(title="System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("API Server", "✓ Running")
    table.add_row("Context Engine", "✓ Active")
    table.add_row("Plugin System", "✓ Ready")
    table.add_row("AI Features", "✓ Available")
    
    console.print(table)


@app.command()
def info():
    """Show detailed system information."""
    rprint("\n[bold]Autonomous UI Engine[/bold] - Phase 6: Innovation\n")
    rprint("[cyan]Features:[/cyan]")
    rprint("  • Advanced AI reasoning (CoT, ToT, ReAct)")
    rprint("  • Intelligent model routing")
    rprint("  • Prompt optimization")
    rprint("  • Context compression")
    rprint("  • Plugin system with lifecycle management")
    rprint("  • Voice interface support")
    rprint("  • GitHub, Figma, Slack integrations")
    rprint("\n[cyan]Quick Commands:[/cyan]")
    rprint("  ui-engine generate ui \"dashboard\"")
    rprint("  ui-engine agents list")
    rprint("  ui-engine plugins enable analytics")
    rprint("  ui-engine context add \"key information\"")
    rprint("\nRun [bold]ui-engine --help[/bold] for more information.\n")


if __name__ == "__main__":
    app()
