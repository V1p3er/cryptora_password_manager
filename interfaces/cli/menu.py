from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def render_header(username: str | None) -> None:
    title = Text("Cryptora Password Manager", style="bold cyan")
    subtitle = (
        f"[green]Logged in:[/green] [bold]{username}[/bold]"
        if username
        else "[yellow]Not logged in[/yellow]"
    )
    console.print(
        Panel.fit(
            f"{subtitle}\n[dim]Type menu number and press Enter[/dim]",
            title=title,
            border_style="bright_blue",
            box=box.ROUNDED,
        )
    )


def render_main_menu() -> None:
    table = Table(box=box.SIMPLE_HEAVY, header_style="bold magenta")
    table.add_column("No", style="bold yellow", justify="center", width=6)
    table.add_column("Action", style="white", min_width=40)

    table.add_row("1", "Register User")
    table.add_row("2", "Login")
    table.add_row("3", "Create Vault")
    table.add_row("4", "Unlock Vault")
    table.add_row("5", "Lock Vault")
    table.add_row("6", "Add Credential")
    table.add_row("7", "List Credentials")
    table.add_row("8", "Get Credential By ID")
    table.add_row("9", "Update Credential")
    table.add_row("10", "Remove Credential")
    table.add_row("11", "Logout")
    table.add_row("0", "Exit")

    console.print(table)


def print_success(message: str) -> None:
    console.print(f"[bold green]SUCCESS:[/bold green] {message}")


def print_error(message: str) -> None:
    console.print(f"[bold red]ERROR:[/bold red] {message}")


def print_info(message: str) -> None:
    console.print(f"[bold cyan]INFO:[/bold cyan] {message}")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")
