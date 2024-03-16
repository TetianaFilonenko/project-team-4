"""Module providing a function printing bot messages."""

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from .input_manager import InputManager
from .address_book import AddressBook
from .edit import edit_record
from .message_manager import print_help_message, print_welcome_message
from .logo import print_ascii_art, logo

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
    "birthdays-for"
    "add-note",
    "find-notes",
    "find-notes-by-tag",
    "delete-note",
    "change-note",
    "all-notes",
    "close",
    "exit",
    "random-book",
    "random-note",
    "edit",
    "about-us",
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

    print_ascii_art(logo)
    print_welcome_message("Welcome to the assistant bot!")
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
            print_help_message()
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
            tags = input("Enter your tags: ")
            print(input_manager.add_note(note, tags))
        elif command == "find-notes":
            keyword = input("Enter searching keyword: ")
            print(input_manager.find_notes(keyword))
        elif command == "find-notes-by-tag":
            tag = input("Enter searching tag: ")
            print(input_manager.find_notes_by_tag(tag))
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
        elif command == "about-us":
            print_ascii_art(logo)
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
