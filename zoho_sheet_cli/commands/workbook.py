"""Workbook management commands."""

import json
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from tabulate import tabulate

from zoho_sheet_cli.client import ZohoSheetClient, ZohoSheetError
from zoho_sheet_cli.config import get_config

console = Console()


@click.group(name="workbook")
def workbook_group():
    """Manage workbooks (spreadsheets)."""
    pass


@workbook_group.command(name="list")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
@click.option("--limit", "-l", type=int, default=100, help="Maximum number of workbooks to list")
def list_workbooks(json_output: bool, limit: int) -> None:
    """List all workbooks."""
    try:
        client = ZohoSheetClient()
        workbooks = client.list_workbooks()
        
        # Limit results
        workbooks = workbooks[:limit]
        
        if json_output:
            click.echo(json.dumps(workbooks, indent=2, ensure_ascii=False))
            return
        
        if not workbooks:
            console.print("[yellow]No workbooks found.[/yellow]")
            return
        
        # Create table
        table = Table(title=f"Workbooks ({len(workbooks)} total)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Owner", style="blue")
        table.add_column("Modified", style="yellow")
        
        for wb in workbooks:
            table.add_row(
                wb.get("resource_id", "N/A"),
                wb.get("workbook_name", "Unnamed"),
                wb.get("owner_email", "Unknown"),
                wb.get("modified_time", "Unknown"),
            )
        
        console.print(table)
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@workbook_group.command(name="create")
@click.option("--name", "-n", required=True, help="Workbook name")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def create_workbook(name: str, json_output: bool) -> None:
    """Create a new workbook."""
    try:
        client = ZohoSheetClient()
        result = client.create_workbook(name)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        workbook_id = result.get("data", {}).get("workbook_id", "Unknown")
        console.print(Panel.fit(
            f"✓ Workbook created successfully!\n\n"
            f"Name: {name}\n"
            f"ID: {workbook_id}",
            title="Success",
            border_style="green",
        ))
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@workbook_group.command(name="info")
@click.argument("workbook_id")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def get_workbook(workbook_id: str, json_output: bool) -> None:
    """Get workbook details."""
    try:
        client = ZohoSheetClient()
        result = client.get_workbook(workbook_id)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        data = result.get("data", {})
        
        table = Table(title="Workbook Details")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", data.get("workbook_id", "N/A"))
        table.add_row("Name", data.get("workbook_name", "N/A"))
        table.add_row("Owner", data.get("owner_email", "N/A"))
        table.add_row("Created", data.get("created_time", "N/A"))
        table.add_row("Modified", data.get("modified_time", "N/A"))
        table.add_row("Sheets", str(data.get("sheet_count", "N/A")))
        
        console.print(table)
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@workbook_group.command(name="delete")
@click.argument("workbook_id")
@click.confirmation_option(
    prompt="Are you sure you want to delete this workbook?",
    help="Confirm deletion",
)
def delete_workbook(workbook_id: str) -> None:
    """Delete a workbook."""
    try:
        client = ZohoSheetClient()
        result = client.delete_workbook(workbook_id)
        
        console.print(f"[green]✓ Workbook {workbook_id} deleted successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@workbook_group.command(name="copy")
@click.argument("workbook_id")
@click.option("--name", "-n", required=True, help="Name for the copied workbook")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def copy_workbook(workbook_id: str, name: str, json_output: bool) -> None:
    """Copy a workbook."""
    try:
        client = ZohoSheetClient()
        result = client.copy_workbook(workbook_id, name)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        new_id = result.get("data", {}).get("workbook_id", "Unknown")
        console.print(Panel.fit(
            f"✓ Workbook copied successfully!\n\n"
            f"New Name: {name}\n"
            f"New ID: {new_id}",
            title="Success",
            border_style="green",
        ))
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@workbook_group.command(name="rename")
@click.argument("workbook_id")
@click.option("--name", "-n", required=True, help="New name for the workbook")
def rename_workbook(workbook_id: str, name: str) -> None:
    """Rename a workbook."""
    try:
        client = ZohoSheetClient()
        result = client.rename_workbook(workbook_id, name)
        
        console.print(f"[green]✓ Workbook renamed to '{name}' successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
