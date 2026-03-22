"""Main CLI entry point for Zoho Sheet CLI."""

import click
from rich.console import Console
from rich.traceback import install

from zoho_sheet_cli.commands.auth import auth_group
from zoho_sheet_cli.commands.workbook import workbook_group
from zoho_sheet_cli.commands.worksheet import worksheet_group
from zoho_sheet_cli.commands.cells import cells_group
from zoho_sheet_cli.commands.files import files_group

# Install rich traceback handler
install(show_locals=True)

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="zsheet")
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
@click.option(
    "--config",
    type=click.Path(),
    help="Path to config file",
)
@click.pass_context
def cli(ctx: click.Context, debug: bool, config: str) -> None:
    """
    Zoho Sheet CLI - Manage your spreadsheets from the command line.
    
    A powerful tool for interacting with Zoho Sheet API v2.
    
    Examples:
        zsheet workbook list
        zsheet workbook create --name "My Workbook"
        zsheet cell get <workbook_id> <sheet> --cell A1
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["config"] = config


# Register command groups
cli.add_command(auth_group)
cli.add_command(workbook_group)
cli.add_command(worksheet_group)
cli.add_command(cells_group)
cli.add_command(files_group)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
