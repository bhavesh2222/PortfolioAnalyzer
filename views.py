from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from contextlib import contextmanager

console = Console()


def show_banner():

    console.print(
        Panel.fit(
            "[bold cyan]Portfolio Analytics Terminal[/bold cyan]\n"
            "[green]Version 1.0[/green]"
        )
    )



def show_portfolio(assets):

    table = Table(title="Current Portfolio")

    table.add_column("Ticker", style="cyan")
    table.add_column("Company", style="green")
    table.add_column("Quantity", justify="right")
    table.add_column("Buy Price", justify="right")

    for asset in assets:

        table.add_row(
            asset.ticker,
            asset.company,
            str(asset.quantity),
            f"${asset.buy_price:.2f}"
        )

    console.print(table)

def show_analysis(rows, summary):

    table = Table(
        title="Portfolio Analysis",
        show_lines=True
    )

    table.add_column("Ticker", style="cyan")
    table.add_column("Company", style="green")
    table.add_column("Qty", justify="right")
    table.add_column("Buy", justify="right")
    table.add_column("Current", justify="right")
    table.add_column("Investment", justify="right")
    table.add_column("Value", justify="right")
    table.add_column("Profit", justify="right")
    table.add_column("Return", justify="right")

    for row in rows:

        profit_style = "green" if row["profit"] >= 0 else "red"

        table.add_row(
            row["ticker"],
            row["company"],
            f"{row['quantity']}",
            f"${row['buy_price']:.2f}",
            f"${row['current_price']:.2f}",
            f"${row['investment']:.2f}",
            f"${row['current_value']:.2f}",
            f"[{profit_style}]${row['profit']:.2f}[/{profit_style}]",
            f"[{profit_style}]{row['return_percent']:.2f}%[/{profit_style}]"
        )

    console.print(table)

    profit_style = (
        "green"
        if summary["profit"] >= 0
        else "red"
    )

    console.print()

    console.print(
        Panel.fit(
            f"""[bold]
            Assets              : {summary['assets']}

            Total Investment    : ${summary['investment']:.2f}

            Current Value       : ${summary['current_value']:.2f}

            Total Profit        : [{profit_style}]${summary['profit']:.2f}[/{profit_style}]

            Overall Return      : [{profit_style}]{summary['return']:.2f}%[/{profit_style}]

            Best Performer      : [green]{summary['best']['ticker']} ({summary['best']['return_percent']:.2f}%)[/green]

            Worst Performer     : [red]{summary['worst']['ticker']} ({summary['worst']['return_percent']:.2f}%)[/red]


            Largest Holding     : [cyan]{summary['largest']['ticker']} (${summary['largest']['current_value']:.2f})[/cyan]
            [/bold]""",
            title="Portfolio Summary",
            border_style="blue"
        )
    )
    


@contextmanager
def loading(message):

    with console.status(f"[bold green]{message}"):

        yield


def show_allocation(rows):

    table = Table(title="Portfolio Allocation")

    table.add_column("Ticker", style="cyan")
    table.add_column("Company", style="green")
    table.add_column("Current Value", justify="right")
    table.add_column("Allocation", justify="right")

    rows.sort(
        key=lambda x: x["allocation"],
        reverse=True
    )

    for row in rows:

        company = row["company"]

        if len(company) > 24:
            company = company[:21] + "..."

        table.add_row(
            row["ticker"],
            company,
            f"${row['value']:.2f}",
            f"{row['allocation']:.2f}%"
        )

    console.print(table)        