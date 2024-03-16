"""Module providing functions for displaying elements with rich library"""

from contextlib import contextmanager
import time
from rich.console import Console
from rich.table import Table
from rich import box
from rich.align import Align
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


console = Console()
BEAT_TIME = 0.04


@contextmanager
def beat(length: int = 1) -> None:
    """
    Pauses execution for a duration determined by the `length` parameter.
    """
    yield
    time.sleep(length * BEAT_TIME)


def print_help_message():
    """
    Prints a help message in table in the console using the Rich library.
    """
    table = Table(title="Available commands:")
    table.title_style = "bold magenta"
    table.box = box.SIMPLE_HEAD
    table.border_style = "bright_yellow"
    table.header_style = "bold bright_blue"
    table_centered = Align.left(table)
    console.clear()
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        with beat(10):
            table.add_column("Name", style="magenta")
            table.add_column("Description", style="green")
        with beat(10):
            table.add_row(
                "hello", ":slightly_smiling_face: Ask the bot how it can help you."
            )
            table.add_row("help", ":question_mark: Shows this help message.")
            table.add_row("close/exit", ":wave: Exits the program.")

        with beat(10):
            table.add_row(
                "add \[name] \[phone]",
                ":telephone_receiver: Adds a contact with the specified name and phone number. Email and address can be added using separate commands.",
            )
            table.add_row(
                "change \[name] \[old-phone] \[phone]",
                ":telephone_receiver: Changes the phone number for the specified contact.",
            )
            table.add_row(
                "phone \[name]",
                ":telephone_receiver: Retrieves the phone number for the specified contact.",
            )
            table.add_row(
                "search \[term]",
                ":magnifying_glass_tilted_left: Global search, retrives any matches in any contact's fields.",
            )
        with beat(10):
            table.add_row(
                "add-email \[name] \[email]",
                ":e-mail: Adds an email to the specified contact.",
            )
            table.add_row(
                "change-email \[name] \[old-email] \[email]",
                ":e-mail: Changes the email for the specified contact.",
            )
            table.add_row(
                "email \[name]",
                ":e-mail: Retrieves the email for the specified contact.",
            )
            table.add_row(
                "add-address \[name] \[address]",
                ":house_with_garden: Adds an address to the specified contact.",
            )
            table.add_row(
                "change-address \[name] \[old-address] \[address]",
                ":house_with_garden: Changes the address for the specified contact.",
            )
            table.add_row(
                "address \[name]",
                ":house_with_garden: Retrieves the address for the specified contact.",
            )
            table.add_row(
                "edit \[fieldname] \[name]",
                ":computer: Edit/Delete phone, email, address.",
            )
            table.add_row("all", ":clipboard: Displays all contacts in the system.")
            table.add_row(
                "random-book",
                ":counterclockwise_arrows_button: Generates random book with 10 contacts.",
            )
        with beat(10):
            table.add_row(
                "add-birthday \[name] \[birthday]",
                ":star: Adds birthday to the contact.",
            )
            table.add_row(
                "show-birthday \[name]", ":star: Shows birthday for specific contact."
            )
            table.add_row(
                "birthdays",
                ":star: Shows birthdays for all contacts celebrating next week.",
            )
        with beat(10):
            table.add_row("add-note", ":spiral_notepad: Adds note to Note Book.")
            table.add_row("find-notes", ":spiral_notepad: Searches notes by keywords.")
            table.add_row(
                "find-notes-by-tag", ":spiral_notepad: Searches notes by tag."
            )
            table.add_row(
                "delete-note", ":spiral_notepad: Deletes note by index in Note Book."
            )
            table.add_row(
                "change-note", ":spiral_notepad: Changes note by index in Note Book."
            )
            table.add_row("all-notes", ":spiral_notepad: Shows all notes in Note Book.")
            table.add_row(
                "random-note",
                ":counterclockwise_arrows_button: Generates random note from Taras Hryhorovych Shevchenko poem",
            )


def print_welcome_message(message):
    """
    Prints a welcome message centered in the console using the Rich library.
    """
    text = Text(message, justify="center")

    panel = Panel(text, expand=True, style="bold blue")
    console.print(panel)
