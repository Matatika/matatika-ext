import webbrowser

import structlog
import typer

from matatika_ext.extension import Matatika

LAB_URL = "https://localhost:3443"

typer.core.rich = None  # remove to enable stylized help output when `rich` is installed
app = typer.Typer()


@app.command()
def start(
    ctx: typer.Context,
):
    """Start the Matatika Lab."""
    ctx.obj["invoke"]("up", "--detach")

    webbrowser.open_new_tab(LAB_URL)


@app.command()
def stop(
    ctx: typer.Context,
    reset: bool = typer.Option(False, help="Clear all data."),
):
    """Stop the Matatika Lab."""
    flags = {
        "-v": reset,
    }

    ctx.obj["invoke"]("down", *[f for f in flags if flags[f]])
