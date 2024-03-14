"""Module providing a function printing bot messages."""

from console_bot.input_manager import InputManager
from console_bot.address_book import AddressBook
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style


def print_help():
    """Function printing help message for bot."""
    help_text = """
Available commands (->/right click is used for autocomplete a command):
  hello                                          - Ask the bot how it can help you.
  add [name] [phone]                             - Adds a contact with the specified name and phone number. Email and address can be added using separate commands.
  change [name] [old-phone] [phone]              - Changes the phone number for the specified contact.
  phone [name]                                   - Retrieves the phone number for the specified contact.
  search [term]                                  - Global search, retrives any matches in any contact's fields.
  add-email [name] [email]                       - Adds an email to the specified contact.
  change-email [name] [old-email ][email]        - Changes the email for the specified contact.
  email [name]                                   - Retrieves the email for the specified contact.
  add-address [name] [address]                   - Adds an address to the specified contact.
  change-address [name] [old-address] [address]  - Changes the address for the specified contact.
  address [name]                                 - Retrieves the address for the specified contact.
  all                                            - Displays all contacts in the system.
  help                                           - Shows this help message.
  add-birthday [name] [birthday]                 - Adds birthday to the contact
  show-birthday [name]                           - Shows birthday for specific contact
  birthdays                                      - Shows birthdays for all contacts celebrating next week
  birthdays-for [days]                           - Shows birthdays for all contacts celebrating in the next amount of days
  add-note                                       - Adds note to Note Book.
  find-notes                                     - Search notes by keywords.
  delete-note                                    - Delete note by index in Note Book.
  edit-note                                      - Edit note by index in Note Book.
  all-notes                                      - Show all notes in Note Book.
  close/exit                                     - Exits the program.
  random-book                                    - Generate random book with 10 contacts.
  random-note                                    - Generate random note from Taras Hryhorovych Shevchenko poem
"""
    print(help_text)


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
    "edit-note",
    "all-notes",
    "close",
    "exit",
    "random-book",
    "random-note",
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
        elif command == "edit-note":
            index = input("Enter index of note you want to change: ")
            new_note = input("Enter a new note: ")
            print(input_manager.edit_note(index, new_note))
        elif command == "all-notes":
            print(input_manager.all_notes())
        elif command == "random-note":
            print_note(input_manager.random_note())
        else:
            print("Invalid command.")
        input_manager.save_to_json()


def print_note(text):
    for line in text.split("\\n"):
        print(line)


if __name__ == "__main__":
    main()
