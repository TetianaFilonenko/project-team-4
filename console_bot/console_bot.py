"""Module providing a function printing bot messages."""

from .input_manager import InputManager
from .address_book import AddressBook
from .edit import edit_record
from rich.console import Console
from rich.table import Table
from rich import box
from rich.align import Align
from rich.live import Live
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
import time
from contextlib import contextmanager


console = Console()
BEAT_TIME = 0.04


@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * BEAT_TIME)


def print_help():
    table = Table(title="Available commands:")
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
            table.add_row("hello", ":wave: Ask the bot how it can help you.")
            table.add_row("help", "Shows this help message.")
            table.add_row("close/exit", "Exits the program.")

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
            table.add_row("edit \[fieldname] \[name]", "Edit/Delete phone, email, address.")
            table.add_row("all", "Displays all contacts in the system.")
            table.add_row("random-book", "Generate random book with 10 contacts.")
        with beat(10):
            table.add_row(
                "add-birthday \[name] \[birthday]", "Adds birthday to the contact."
            )
            table.add_row(
                "show-birthday \[name]", "Shows birthday for specific contact."
            )
            table.add_row(
                "birthdays", "Shows birthdays for all contacts celebrating next week."
            )
        with beat(10):
            table.add_row("add-note", ":spiral_notepad: Adds note to Note Book.")
            table.add_row("find-notes", ":spiral_notepad: Searches notes by keywords.")
            table.add_row(
                "delete-note", ":spiral_notepad: Deletes note by index in Note Book."
            )
            table.add_row(
                "change-note", ":spiral_notepad: Changes note by index in Note Book."
            )
            table.add_row("all-notes", ":spiral_notepad: Shows all notes in Note Book.")
            table.add_row(
                "random-note",
                ":spiral_notepad: Generates random note from Taras Hryhorovych Shevchenko poem",
            )

commands = [
    "hello",
    "add",
    "change",
    "phone",
    "search",
    "add-email",
    "change-email",
    "email",
    "add-address",
    "change-address",
    "address",
    "all",
    "help",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-note",
    "find-notes",
    "delete-note",
    "change-note",
    "all-notes",
    "close",
    "exit",
    "random-book",
    "random-note",
    "edit",
]
style = Style.from_dict({"": "#1cb649 italic bold"})


def main():
    """Central function printing all the commands"""
    input_manager = InputManager()
    history = InMemoryHistory()
    for command in commands:
        history.append_string(command)
    session = PromptSession(
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
    )
    print("Welcome to the assistant bot!")
    print(AddressBook().check_today_birthdays())
    print_note(input_manager.random_note(save=False))

    while True:
        try:
            user_input = session.prompt("Enter a command: ", style=style)
            command, *args = input_manager.parse_input(user_input)
        except KeyboardInterrupt:
            print("Ctrl-C pressed. Try again.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            input_manager.save_to_json()
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(input_manager.add_contact(args))
        elif command == "change":
            print(input_manager.change_contact(args))
        elif command == "phone":
            print(input_manager.get_contact_phone(args))
        elif command == "search":
            print(input_manager.full_search(args))
        elif command == "add-email":
            print(input_manager.add_contact_email(args))
        elif command == "change-email":
            print(input_manager.change_contact_email(args))
        elif command == "email":
            print(input_manager.get_contact_email(args))
        elif command == "add-address":
            print(input_manager.add_contact_address(args))
        elif command == "change-address":
            new_address = input("Enter new address: ")
            print(input_manager.change_contact_address(args, new_address))
        elif command == "address":
            print(input_manager.get_contact_address(args))
        elif command == "all":
            print(input_manager.get_all_contacts())
        elif command == "help":
            print_help()
        elif command == "add-birthday":
            print(input_manager.add_birthday(args))
        elif command == "show-birthday":
            print(input_manager.show_birthday(args))
        elif command == "birthdays":
            print(input_manager.get_next_week_birthdays())
        elif command == "birthdays-for":
            print(input_manager.get_birthdays_for_amount_days(args))
        elif command == "random-book":
            print(input_manager.generate_random_book())
        elif command == "add-note":
            note = input("Enter your note: ")
            print(input_manager.add_note(note))
        elif command == "find-notes":
            keyword = input("Enter searching keyword: ")
            print(input_manager.find_notes(keyword))
        elif command == "delete-note":
            index = input("Enter index of note you want to remove: ")
            print(input_manager.delete_note(index))
        elif command == "change-note":
            index = input("Enter index of note you want to change: ")
            new_note = input("Enter a new note: ")
            print(input_manager.edit_note(index, new_note))
        elif command == "all-notes":
            print(input_manager.all_notes())
        elif command == "random-note":
            print_note(input_manager.random_note())
        elif command == "edit":
            edit_record(input_manager, args)
        else:
            print("Invalid command.")
        input_manager.save_to_json()


def print_note(text: str):
    """
    Function to print a note to the console in a readable format.
    """
    for line in text.split("\\n"):
        print(line)


if __name__ == "__main__":
    main()
