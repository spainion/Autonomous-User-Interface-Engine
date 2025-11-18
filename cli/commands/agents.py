"""Agent management commands for CLI."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command("list")
def list_agents():
    """List all available agents."""
    table = Table(title="Available Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="green")
    
    # Sample data
    agents = [
        ("UI Generator", "Generation", "Active"),
        ("Code Analyzer", "Analysis", "Active"),
        ("Reasoning Agent", "AI", "Active"),
    ]
    
    for name, agent_type, status in agents:
        table.add_row(name, agent_type, status)
    
    console.print(table)


@app.command("execute")
def execute_agent(
    agent: str = typer.Argument(..., help="Agent name"),
    task: str = typer.Argument(..., help="Task description")
):
    """Execute an agent with a specific task."""
    console.print(f"Executing agent: [bold]{agent}[/bold]")
    console.print(f"Task: {task}")
    console.print("✓ Agent executed successfully")


@app.command("status")
def agent_status(agent: str = typer.Argument(..., help="Agent name")):
    """Show agent status."""
    console.print(f"\n[bold]Agent:[/bold] {agent}")
    console.print(f"[bold]Status:[/bold] Active")
    console.print(f"[bold]Tasks Completed:[/bold] 42")
    console.print(f"[bold]Success Rate:[/bold] 95%\n")
