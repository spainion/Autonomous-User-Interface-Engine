"""Plugin management commands for CLI."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command("list")
def list_plugins():
    """List all available plugins."""
    table = Table(title="Installed Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Status", style="green")
    
    plugins = [
        ("analytics-plugin", "1.0.0", "Enabled"),
        ("custom-ui-plugin", "1.0.0", "Enabled"),
        ("notification-plugin", "1.0.0", "Disabled"),
    ]
    
    for name, version, status in plugins:
        table.add_row(name, version, status)
    
    console.print(table)


@app.command("enable")
def enable_plugin(name: str = typer.Argument(..., help="Plugin name")):
    """Enable a plugin."""
    console.print(f"Enabling plugin: [bold]{name}[/bold]")
    console.print("✓ Plugin enabled successfully")


@app.command("disable")
def disable_plugin(name: str = typer.Argument(..., help="Plugin name")):
    """Disable a plugin."""
    console.print(f"Disabling plugin: [bold]{name}[/bold]")
    console.print("✓ Plugin disabled successfully")


@app.command("install")
def install_plugin(
    path: str = typer.Argument(..., help="Plugin path or name")
):
    """Install a new plugin."""
    console.print(f"Installing plugin from: [bold]{path}[/bold]")
    console.print("✓ Plugin installed successfully")


@app.command("info")
def plugin_info(name: str = typer.Argument(..., help="Plugin name")):
    """Show plugin information."""
    console.print(f"\n[bold]Plugin:[/bold] {name}")
    console.print(f"[bold]Version:[/bold] 1.0.0")
    console.print(f"[bold]Author:[/bold] UI Engine Team")
    console.print(f"[bold]Description:[/bold] Example plugin")
    console.print(f"[bold]Status:[/bold] Enabled\n")
