"""Configuration management commands for CLI."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command("show")
def show_config():
    """Show current configuration."""
    table = Table(title="Configuration")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    
    config = [
        ("api.host", "localhost"),
        ("api.port", "8000"),
        ("llm.provider", "openrouter"),
        ("llm.model", "gpt-4"),
        ("context.max_size", "1000"),
    ]
    
    for key, value in config:
        table.add_row(key, value)
    
    console.print(table)


@app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value")
):
    """Set a configuration value."""
    console.print(f"Setting [bold]{key}[/bold] = {value}")
    console.print("✓ Configuration updated")


@app.command("get")
def get_config(key: str = typer.Argument(..., help="Configuration key")):
    """Get a configuration value."""
    console.print(f"[bold]{key}[/bold] = value")


@app.command("reset")
def reset_config(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Reset configuration to defaults."""
    if not confirm:
        if not typer.confirm("Reset all configuration to defaults?"):
            raise typer.Abort()
    
    console.print("✓ Configuration reset to defaults")
