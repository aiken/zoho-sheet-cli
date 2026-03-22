"""Authentication commands."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from zoho_sheet_cli.config import Config, get_config

console = Console()


@click.group(name="auth")
def auth_group():
    """Manage authentication settings."""
    pass


@auth_group.command()
@click.option(
    "--client-id",
    prompt="Enter your Zoho Client ID",
    help="Zoho OAuth2 Client ID",
)
@click.option(
    "--client-secret",
    prompt="Enter your Zoho Client Secret",
    hide_input=True,
    help="Zoho OAuth2 Client Secret",
)
@click.option(
    "--refresh-token",
    prompt="Enter your Zoho Refresh Token",
    hide_input=True,
    help="Zoho OAuth2 Refresh Token",
)
@click.option(
    "--region",
    type=click.Choice(["us", "eu", "in", "cn", "au", "jp"]),
    default="us",
    help="Zoho region (us, eu, in, cn, au, jp)",
)
def init(client_id: str, client_secret: str, refresh_token: str, region: str) -> None:
    """Initialize authentication configuration."""
    config = get_config()
    config.client_id = client_id
    config.client_secret = client_secret
    config.refresh_token = refresh_token
    config.region = region
    config.save()
    
    console.print(Panel.fit(
        "[OK] Authentication configuration saved successfully!\n\n"
        f"Configuration file: {config.config_path}\n"
        f"Region: {region.upper()}",
        title="Success",
        border_style="green",
    ))


@auth_group.command()
def status() -> None:
    """Check authentication status."""
    config = get_config()
    
    table = Table(title="Authentication Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Status", style="yellow")
    
    # Client ID
    client_id_status = "[OK]" if config.client_id else "[MISSING]"
    client_id_display = config.client_id[:10] + "..." if config.client_id else "Not set"
    table.add_row("Client ID", client_id_display, client_id_status)
    
    # Client Secret
    secret_status = "[OK]" if config.client_secret else "[MISSING]"
    secret_display = "*" * 10 if config.client_secret else "Not set"
    table.add_row("Client Secret", secret_display, secret_status)
    
    # Refresh Token
    token_status = "[OK]" if config.refresh_token else "[MISSING]"
    token_display = config.refresh_token[:10] + "..." if config.refresh_token else "Not set"
    table.add_row("Refresh Token", token_display, token_status)
    
    # Region
    table.add_row("Region", config.region.upper(), "[OK]")
    
    console.print(table)
    
    if config.is_authenticated:
        console.print("\n[green][OK] Authentication is configured correctly.[/green]")
    else:
        console.print(
            "\n[red][FAIL] Authentication is incomplete. "
            "Please run 'zsheet auth init' to configure.[/red]"
        )


@auth_group.command()
def refresh() -> None:
    """Refresh access token."""
    from zoho_sheet_cli.client import ZohoSheetClient
    
    try:
        client = ZohoSheetClient()
        console.print("[green][OK] Access token refreshed successfully![/green]")
    except Exception as e:
        console.print(f"[red][FAIL] Failed to refresh token: {e}[/red]")


@auth_group.command()
def guide() -> None:
    """Show guide for getting Zoho API credentials."""
    guide_text = """
[bold cyan]How to get Zoho API Credentials:[/bold cyan]

[bold]Step 1: Create Client in API Console[/bold]
1. Visit https://api-console.zoho.com/
2. Click "Add Client" -> "Server-based Applications"
3. Fill in:
   - Client Name: Zoho Sheet CLI
   - Homepage URL: (optional)
   - Authorized Redirect URIs: http://localhost:8080/callback
4. Click "Create" and save Client ID and Client Secret

[bold]Step 2: Get Authorization Code[/bold]
Visit this URL in your browser:
[link]https://accounts.zoho.com/oauth/v2/auth?response_type=code&client_id=YOUR_CLIENT_ID&scope=ZohoSheet.dataAPI.ALL&redirect_uri=http://localhost:8080/callback&access_type=offline&prompt=consent[/link]

Or use this scope for specific permissions:
- ZohoSheet.dataAPI.READ (read workbooks/sheets)
- ZohoSheet.dataAPI.CREATE (create workbooks/sheets)
- ZohoSheet.dataAPI.UPDATE (update cells/data)
- ZohoSheet.dataAPI.DELETE (delete workbooks/sheets)
- ZohoSheet.dataAPI.ALL (full access - recommended)

After authorization, copy the "code" from the redirect URL.

[bold]Step 3: Exchange Code for Tokens[/bold]
Run this curl command:
[code]
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \\
  -d "code=YOUR_AUTH_CODE" \\
  -d "client_id=YOUR_CLIENT_ID" \\
  -d "client_secret=YOUR_CLIENT_SECRET" \\
  -d "redirect_uri=http://localhost:8080/callback" \\
  -d "grant_type=authorization_code"
[/code]

[bold]Step 4: Save Refresh Token[/bold]
From the response, save the "refresh_token" value.

[bold green]Now run: zsheet auth init[/bold green] to configure.
"""
    console.print(Panel(guide_text, title="API Credentials Guide", border_style="blue"))
