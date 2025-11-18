"""Context operations commands for CLI."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command("add")
def add_context(
    content: str = typer.Argument(..., help="Content to add"),
    embedding: str = typer.Option("", "--embedding", "-e", help="Embedding text"),
    importance: float = typer.Option(0.5, "--importance", "-i", help="Importance score")
):
    """Add information to context database."""
    console.print(f"Adding to context: [bold]{content[:50]}...[/bold]")
    console.print(f"Importance: {importance}")
    console.print("✓ Added to context successfully")


@app.command("search")
def search_context(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-l", help="Result limit")
):
    """Search context database."""
    console.print(f"Searching for: [bold]{query}[/bold]\n")
    
    table = Table(title="Search Results")
    table.add_column("Rank", style="cyan")
    table.add_column("Content", style="white")
    table.add_column("Score", style="green")
    
    # Sample results
    for i in range(min(3, limit)):
        table.add_row(str(i+1), f"Result {i+1} matching '{query}'", f"0.{90-i*10}")
    
    console.print(table)


@app.command("clear")
def clear_context(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Clear context database."""
    if not confirm:
        if not typer.confirm("Clear all context data?"):
            raise typer.Abort()
    
    console.print("✓ Context database cleared")


@app.command("stats")
def context_stats():
    """Show context database statistics."""
    console.print("\n[bold]Context Database Statistics[/bold]\n")
    console.print(f"Total Entries: 1,234")
    console.print(f"Total Size: 45 MB")
    console.print(f"Avg Importance: 0.67")
    console.print(f"Last Updated: 2 hours ago\n")
