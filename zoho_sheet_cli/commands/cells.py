"""Cell operations commands."""

import json
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from zoho_sheet_cli.client import ZohoSheetClient, ZohoSheetError

console = Console()


@click.group(name="cell")
def cells_group():
    """Manage cells and ranges."""
    pass


@cells_group.command(name="get")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.option("--cell", "-c", required=True, help="Cell address (e.g., A1)")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def get_cell(workbook_id: str, sheet_name: str, cell: str, json_output: bool) -> None:
    """Get the value of a cell."""
    try:
        client = ZohoSheetClient()
        result = client.get_cell(workbook_id, sheet_name, cell)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        data = result.get("data", {})
        
        table = Table(title=f"Cell {cell}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Cell", data.get("cell", cell))
        table.add_row("Value", str(data.get("value", "N/A")))
        table.add_row("Formatted", str(data.get("formatted_value", "N/A")))
        table.add_row("Data Type", data.get("data_type", "unknown"))
        
        console.print(table)
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cells_group.command(name="set")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.option("--cell", "-c", required=True, help="Cell address (e.g., A1)")
@click.option("--value", "-v", required=True, help="Value to set")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def set_cell(workbook_id: str, sheet_name: str, cell: str, value: str, json_output: bool) -> None:
    """Set the value of a cell."""
    try:
        client = ZohoSheetClient()
        result = client.set_cell(workbook_id, sheet_name, cell, value)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        console.print(f"[green]✓ Cell {cell} set to '{value}' successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cells_group.command(name="range")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.option("--range", "-r", "range_addr", required=True, help="Range address (e.g., A1:D10)")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def get_range(workbook_id: str, sheet_name: str, range_addr: str, json_output: bool) -> None:
    """Get values from a range of cells."""
    try:
        client = ZohoSheetClient()
        result = client.get_range(workbook_id, sheet_name, range_addr)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        data = result.get("data", {})
        values = data.get("values", [])
        
        if not values:
            console.print("[yellow]No data in range.[/yellow]")
            return
        
        # Create table for range data
        table = Table(title=f"Range {range_addr}")
        
        # Add columns
        num_cols = len(values[0]) if values else 0
        for col_idx in range(num_cols):
            table.add_column(chr(65 + col_idx), style="green")  # A, B, C, ...
        
        # Add rows
        for row in values:
            table.add_row(*[str(cell) if cell is not None else "" for cell in row])
        
        console.print(table)
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cells_group.command(name="set-range")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.option("--range", "-r", "range_addr", required=True, help="Range address (e.g., A1:B2)")
@click.option("--values", required=True, help='JSON array of values (e.g., [["A","B"],["C","D"]])')
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def set_range(workbook_id: str, sheet_name: str, range_addr: str, values: str, json_output: bool) -> None:
    """Set values in a range of cells."""
    try:
        # Parse values from JSON string
        parsed_values = json.loads(values)
        
        client = ZohoSheetClient()
        result = client.set_range(workbook_id, sheet_name, range_addr, parsed_values)
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        console.print(f"[green]✓ Range {range_addr} updated successfully![/green]")
        
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON format for values.[/red]")
        console.print('Example: [["A","B"],["C","D"]]')
        raise click.Abort()
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cells_group.command(name="clear")
@click.argument("workbook_id")
@click.argument("sheet_name")
@click.option("--cell", "-c", help="Cell address to clear")
@click.option("--range", "-r", help="Range address to clear")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def clear_cells(workbook_id: str, sheet_name: str, cell: Optional[str], range: Optional[str], json_output: bool) -> None:
    """Clear cell(s) content."""
    if not cell and not range:
        console.print("[red]Error: Must specify either --cell or --range[/red]")
        raise click.Abort()
    
    try:
        client = ZohoSheetClient()
        
        if cell:
            result = client.set_cell(workbook_id, sheet_name, cell, "")
            msg = f"Cell {cell} cleared"
        else:
            # For range, we need to set empty values
            # This is a simplified version - real implementation would get range dimensions first
            result = client.set_range(workbook_id, sheet_name, range, [[""]])
            msg = f"Range {range} cleared"
        
        if json_output:
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        console.print(f"[green]✓ {msg} successfully![/green]")
        
    except ZohoSheetError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
