from rich.console import Console
from rich.logging import RichHandler
from pathlib import Path
import logging

# Setup Rich Console
console = Console()

# Setup Logging
LOG_FILE = "/.nucleus/nucleus.log"
logging.basicConfig(
    level=logging.ERROR,  # Set the default log level
    format="%(message)s",
    handlers=[
        RichHandler(console=console, rich_tracebacks=True, markup=True),  # Rich formatting for console
        # logging.FileHandler(LOG_FILE)  # Save logs to a file
    ]
)

# Get Logger
log = logging.getLogger("rich_logger")

# Example log messages
def log_examples():
    log.debug("This is a [bold green]DEBUG[/bold green] message for internal debugging.")
    log.info("This is an [cyan]INFO[/cyan] message for general information.")
    log.warning("This is a [yellow]WARNING[/yellow] message indicating potential issues.")
    log.error("This is an [bold red]ERROR[/bold red] message for serious problems.")
    log.critical("This is a [bold red on white]CRITICAL[/bold red on white] message for severe issues.")

if __name__ == "__main__":

    log_examples()
    console.print(f"[green]Log messages have been saved to[/green] {LOG_FILE}.")
