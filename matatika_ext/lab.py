import threading
import time
import webbrowser

import requests
import typer

from matatika_ext.extension import log

LAB_URL = "https://localhost:3443"

typer.core.rich = None  # remove to enable stylized help output when `rich` is installed
app = typer.Typer()


@app.callback(invoke_without_command=True)
def default(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand:
        return

    def open_app_in_browser(poll_seconds: float = 5, timeout_seconds: float = 300):
        start_time = time.time()

        while True:
            if time.time() > start_time + timeout_seconds:
                log.error(
                    f"Timed out waiting {timeout_seconds:.2f}s for {LAB_URL} - will not open in default browser"
                )
                return

            try:
                if requests.get(LAB_URL, verify=False).status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                continue
            finally:
                log.debug(f"Waiting for {LAB_URL} ({time.time() - start_time:.2f}s)")
                time.sleep(poll_seconds)

        webbrowser.open_new_tab(LAB_URL)
        log.debug(
            f"Opened {LAB_URL} in default browser (completed in {time.time() - start_time:.2f}s))"
        )

    threading.Thread(target=open_app_in_browser).start()
    ctx.obj["invoke"]("up")


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
        "--remove-orphans": reset,
    }

    ctx.obj["invoke"]("down", *[f for f in flags if flags[f]])
