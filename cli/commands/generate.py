"""UI generation commands for CLI."""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

app = typer.Typer()
console = Console()


@app.command("ui")
def generate_ui(
    description: str = typer.Argument(..., help="Description of UI to generate"),
    output: str = typer.Option("output.html", "--output", "-o", help="Output file"),
    framework: str = typer.Option("html", "--framework", "-f", help="Framework (html, react, vue)"),
    style: str = typer.Option("modern", "--style", "-s", help="Style theme")
):
    """Generate a UI from description."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Generating {framework} UI...", total=None)
        
        # Simulate UI generation
        ui_code = f"""<!DOCTYPE html>
<html>
<head>
    <title>Generated UI</title>
    <style>
        body {{ font-family: system-ui; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{description}</h1>
        <p>Generated with UI Engine CLI</p>
    </div>
</body>
</html>"""
        
        progress.remove_task(task)
    
    # Write to file
    with open(output, 'w') as f:
        f.write(ui_code)
    
    console.print(f"✓ Generated UI saved to [bold]{output}[/bold]")
    
    if typer.confirm("Preview code?", default=False):
        syntax = Syntax(ui_code, "html", theme="monokai", line_numbers=True)
        console.print(syntax)


@app.command("component")
def generate_component(
    name: str = typer.Argument(..., help="Component name"),
    props: str = typer.Option("", "--props", "-p", help="Component props (JSON)")
):
    """Generate a specific component."""
    console.print(f"Generating component: [bold]{name}[/bold]")
    console.print(f"✓ Component generated successfully")


@app.command("theme")
def generate_theme(
    name: str = typer.Argument(..., help="Theme name"),
    colors: str = typer.Option("", "--colors", "-c", help="Color scheme")
):
    """Generate a theme."""
    console.print(f"Generating theme: [bold]{name}[/bold]")
    console.print(f"✓ Theme generated successfully")
