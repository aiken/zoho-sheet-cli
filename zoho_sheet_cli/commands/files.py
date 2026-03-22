"""File operations commands."""

import os
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from zoho_sheet_cli.client import ZohoSheetClient, ZohoSheetError

console = Console()


@click.group(name="file")
def files_group():
    """Import and export files."""
    pass


@files_group.command(name="export")
@click.argument("workbook_id")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["xlsx", "xls", "csv", "pdf", "ods", "html", "tsv"]),
    default="xlsx",
    help="Export format",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: workbook_name.format)",
)
@click.option("--sheet", "-s", help="Sheet name (for CSV export)")
def export_workbook(workbook_id: str, format: str, output: str, sheet: str) -> None:
    """Export a workbook to a file."""
    try:
        client = ZohoSheetClient()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Exporting workbook...", total=None)
            
            content = client.export_workbook(workbook_id, format)
        
        # Determine output filename
        if not output:
            # Try to get workbook name
            try:
                info = client.get_workbook(workbook_id)
                workbook_name = info.get("data", {}).get("workbook_name", workbook_id)
            except:
                workbook_name = workbook_id
            output = f"{workbook_name}.{format}"
        
        # Save file
        output_path = Path(output)
        output_path.write_bytes(content)
        
        file_size = len(content)
        size_str = f"{file_size / 1024:.1f} KB" if file_size > 1024 else f"{file_size} bytes"
        
        console.print(f"[green]✓ Exported to {output} ({size_str})[/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@files_group.command(name="import")
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, readable=True),
    required=True,
    help="File to import",
)
@click.option(
    "--name",
    "-n",
    help="Name for the new workbook (default: filename without extension)",
)
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def import_file(file: str, name: str, json_output: bool) -> None:
    """Import a file as a new workbook."""
    import json as json_mod
    
    file_path = Path(file)
    
    # Validate file extension
    supported_extensions = {".csv", ".xls", ".xlsx", ".ods", ".tsv", ".html"}
    if file_path.suffix.lower() not in supported_extensions:
        console.print(
            f"[red]Error: Unsupported file format '{file_path.suffix}'. "
            f"Supported: {', '.join(supported_extensions)}[/red]"
        )
        raise click.Abort()
    
    try:
        client = ZohoSheetClient()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Importing file...", total=None)
            
            result = client.import_file(str(file_path), name)
        
        if json_output:
            click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
            return
        
        workbook_id = result.get("data", {}).get("workbook_id", "Unknown")
        workbook_name = result.get("data", {}).get("workbook_name", "Unknown")
        
        console.print(f"[green]✓ File imported successfully![/green]")
        console.print(f"  Name: {workbook_name}")
        console.print(f"  ID: {workbook_id}")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@files_group.command(name="download")
@click.argument("workbook_id")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["xlsx", "xls", "csv", "pdf", "ods"]),
    default="xlsx",
    help="Download format",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output directory (default: current directory)",
)
def download_workbook(workbook_id: str, format: str, output: str) -> None:
    """Download a workbook (alias for export)."""
    ctx = click.get_current_context()
    ctx.invoke(export_workbook, workbook_id=workbook_id, format=format, output=output, sheet=None)
