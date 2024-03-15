# Console Bot

Console Bot is a command-line application designed to assist users with managing contacts, notes, and birthdays. It provides a set of commands for adding, modifying, and retrieving information from an address book and a note book.

## Installation

Clone the repository:

```bash
git clone https://github.com/TetianaFilonenko/project-team-4.git
```

Navigate to the project directory:

```bash
cd console_bot
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

To run the Console Bot application as a package, execute the following command:

```bash
python3 -m venv env
source env/bin/activate
pip3 install -e .
run-console-bot
```

## Available Commands

Console Bot supports the following commands:

| Command                                         | Description                                                              |
| ----------------------------------------------- | ------------------------------------------------------------------------ |
| `hello`                                         | Greets the user and asks how it can help.                                |
| `add [name] [phone]`                            | Adds a contact with the specified name and phone number.                 |
| `change [name] [old-phone] [phone]`             | Changes the phone number for the specified contact.                      |
| `phone [name]`                                  | Retrieves the phone number for the specified contact.                    |
| `search [term]`                                 | Global search, retrieves any matches in any contact's fields.            |
| `add-email [name] [email]`                      | Adds an email to the specified contact.                                  |
| `change-email [name] [old-email] [email]`       | Changes the email for the specified contact.                             |
| `email [name]`                                  | Retrieves the email for the specified contact.                           |
| `add-address [name] [address]`                  | Adds an address to the specified contact.                                |
| `change-address [name] [old-address] [address]` | Changes the address for the specified contact.                           |
| `address [name]`                                | Retrieves the address for the specified contact.                         |
| `all`                                           | Displays all contacts in the system.                                     |
| `help`                                          | Shows this help message.                                                 |
| `add-birthday [name] [birthday]`                | Adds birthday to the contact.                                            |
| `show-birthday [name]`                          | Shows birthday for specific contact.                                     |
| `birthdays`                                     | Shows birthdays for all contacts celebrating next week.                  |
| `birthdays-for [days]`                          | Shows birthdays for all contacts celebrating in the next amount of days. |
| `add-note`                                      | Adds note to Note Book.                                                  |
| `find-notes`                                    | Search notes by keywords.                                                |
| `delete-note`                                   | Delete note by index in Note Book.                                       |
| `edit-note`                                     | Edit note by index in Note Book.                                         |
| `all-notes`                                     | Show all notes in Note Book.                                             |
| `close/exit`                                    | Exits the program.                                                       |
| `random-book`                                   | Generate random book with 10 contacts.                                   |
| `random-note`                                   | Generate random note from Taras Hryhorovych Shevchenko poem.             |
