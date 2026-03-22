"""Worksheet management commands."""

import json

import click
from rich.console import Console
from rich.table import Table

from zoho_sheet_cli.client import ZohoSheetClient, ZohoSheetError

console = Console()


@click.group(name="worksheet")
def worksheet_group():
    """Manage worksheets (sheets within a workbook)."""
    pass


@worksheet_group.command(name="list")
@click.argument("workbook_id")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def list_worksheets(workbook_id: str, json_output: bool) -> None:
    """List all worksheets in a workbook."""
    try:
        client = ZohoSheetClient()
        worksheets = client.list_worksheets(workbook_id)
        
        if json_output:
            click.echo(json.dumps(worksheets, indent=2, ensure_ascii=False))
            return
        
        if not worksheets:
            console.print("[yellow]No worksheets found.[/yellow]")
            return
        
        table = Table(title=f"Worksheets in Workbook {workbook_id}")
        table.add_column("Name", style="cyan")
        table.add_column("Visibility", style="green")
        
        for ws in worksheets:
            table.add_row(
                ws.get("sheet_name", "Unnamed"),
                ws.get("visibility", "visible"),
            )
        
        console.print(table)
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@worksheet_group.command(name="add")
@click.argument("workbook_id")
@click.option("--name", "-n", required=True, help="Worksheet name")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def add_worksheet(workbook_id: str, name: str, json_output: bool) -> None:
    """Add a new worksheet to a workbook."""
    try:
        client = ZohoSheetClient()
        result = client.add_worksheet(workbook_id, name)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        console.print(f"[green]✓ Worksheet '{name}' added successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@worksheet_group.command(name="delete")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.confirmation_option(
    prompt="Are you sure you want to delete this worksheet?",
    help="Confirm deletion",
)
def delete_worksheet(workbook_id: str, sheet_name: str) -> None:
    """Delete a worksheet from a workbook."""
    try:
        client = ZohoSheetClient()
        result = client.delete_worksheet(workbook_id, sheet_name)
        
        console.print(f"[green]✓ Worksheet '{sheet_name}' deleted successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@worksheet_group.command(name="rename")
@click.argument("workbook_id")
@click.argument("old_name")
@click.option("--new", "new_name", required=True, help="New worksheet name")
def rename_worksheet(workbook_id: str, old_name: str, new_name: str) -> None:
    """Rename a worksheet."""
    try:
        client = ZohoSheetClient()
        result = client.rename_worksheet(workbook_id, old_name, new_name)
        
        console.print(
            f"[green]✓ Worksheet renamed from '{old_name}' to '{new_name}' "
            f"successfully![/green]"
        )
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
