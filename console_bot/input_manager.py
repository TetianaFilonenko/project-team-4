from .errors import input_error
from .note import NoteBook, Note
from .address_book import Record, AddressBook


class InputManager:
    """
    Class-delegator that stores all the input managing objects for a bot
    """

    def __init__(self):
        self.book = AddressBook.load_from_file("address_book.json")
        self.note_book = NoteBook.load_from_file("note_book.json")

    @input_error
    def parse_input(self, user_input: str):
        """
        Function to parse user input by splitting it into command and arguments
        """
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, args: list[str]):
        """
        Function to add a contact and phone number to the address book.
        """
        name, phone = args
        new_record = Record(name)
        isvalid, message = new_record.add_phone(phone)
        if isvalid:
            self.book.add_contact(new_record)
        return message

    @input_error
    def change_contact(self, args: list[str]):
        """
        Function to change a phone number of a contact in the address book.
        """
        name, old_phone, new_phone = args
        return self.book.change_contact(name, old_phone, new_phone)

    @input_error
    def get_contact_phone(self, args: list[str]):
        """
        Function to get a phone number of a contact in the address book.
        """
        name = args[0]
        return self.book.find(name)

    @input_error
    def full_search(self, args: list[str]):
        """
        Function to find all contacts containing a specific term.
        """
        term = args[0]
        return self.book.find_all(term)

    def get_all_contacts(self):
        """
        Function to get all contacts in the address book and return them as a string sorted by name.
        """
        return "\n".join(sorted(map(str, self.book.data.values())))

    @input_error
    def add_birthday(self, args: list[str]):
        """
        Function to add a birthday to a contact in the address book.
        """
        name, birthday = args
        new_record = Record(name)
        isvalid, message = new_record.add_birthday(birthday)
        if isvalid:
            self.book.add_birthday(new_record)
        return message

    @input_error
    def show_birthday(self, args: list[str]):
        """
        Function to show the birthday of a contact in the address book.
        """
        name = args[0]
        return self.book.show_birthday(name)

    def get_next_week_birthdays(self):
        """
        Function to get all birthdays in the next week and return them as a string.
        """
        return self.book.get_next_week_birthdays()

    def get_birthdays_for_amount_days(self, args: list[str]):
        """
        Function to get all birthdays in the next number of days and return them as a string.
        """
        days = args[0]
        return self.book.get_birthdays_for_amount_days(days)

    @input_error
    def add_contact_email(self, args: list[str]):
        """
        Function to add an email to a contact in the address book.
        """
        name, email = args
        return self.book.add_email(name, email)

    @input_error
    def change_contact_email(self, args: list[str]):
        """
        Function to change an email of a contact in the address book.
        """
        name, old_email, new_email = args
        return self.book.change_email(name, old_email, new_email)

    @input_error
    def get_contact_email(self, args: list[str]):
        """
        Function to get an email of a contact in the address book.
        """
        name = args[0]
        return self.book.get_email(name)

    @input_error
    def add_contact_address(self, args: list[str]):
        """
        Function to add an address to a contact in the address book.
        """
        name, *address_parts = args
        address = " ".join(address_parts)
        return self.book.add_address(name, address)

    @input_error
    def change_contact_address(self, args: list[str], new_address: str):
        """
        Function to change an address of a contact in the address book.
        """
        name, *address_parts = args
        old_address = " ".join(address_parts)
        return self.book.change_address(name, old_address, new_address)

    @input_error
    def get_contact_address(self, args: list[str]):
        """
        Function to get an address of a contact in the address book.
        """
        name = args[0]
        return self.book.get_address(name)

    def generate_random_book(self):
        """
        Function to generate random data for the address book.
        """
        self.book.generate_random_data()
        return self.get_all_contacts()

    @input_error
    def add_note(self, value: str):
        """
        Function to add a note to the notebook.
        """
        return self.note_book.add_note(Note(value))

    @input_error
    def find_notes(self, keyword: str):
        """
        Function to find notes containing a specific keyword.
        """
        return self.note_book.find_notes(keyword)

    @input_error
    def change_note(self, index: str, new_note: str):
        """
        Function to change a note at a specific index.
        """
        index = int(index)
        return self.note_book.edit_note(index, new_note)

    @input_error
    def delete_note(self, index: str):
        """
        Function to delete a note at a specific index.
        """
        index = int(index)
        return self.note_book.delete_note(int(index))

    def all_notes(self):
        """
        Function to get all notes in the notebook and return them as a string sorted by value.
        """
        return str(self.note_book)

    def random_note(self, save=True):
        """
        Function to generate a note with a random quote from Shevchenko poem.
        """
        return self.note_book.generate_random(save)

    def save_to_json(self):
        """
        Function to save the address book and notebook to JSON files.
        """
        self.book.save_to_file()
        self.note_book.save_to_file()
