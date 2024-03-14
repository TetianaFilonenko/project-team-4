from .errors import input_error
from .note import NoteBook, Note
from .address_book import Record, AddressBook
import json


class InputManager:
    def __init__(self):
        self.book = AddressBook.load_from_file('address_book.json')
        self.note_book = NoteBook.load_from_file('note_book.json')

    @input_error
    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, args):
        name, phone = args
        new_record = Record(name)
        isvalid, message = new_record.add_phone(phone)
        if isvalid:
            self.book.add_contact(new_record)
        return message

    @input_error
    def change_contact(self, args):
        name, old_phone, new_phone = args
        return self.book.change_contact(name, old_phone, new_phone)

    @input_error
    def get_contact_phone(self, args):
        name = args[0]
        return self.book.find(name)
    
    @input_error
    def full_search(self, args):
        term = args[0]
        return self.book.find_all(term)

    def get_all_contacts(self):
        return "\n".join(map(str, self.book.data.values()))

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        new_record = Record(name)
        isvalid, message = new_record.add_birthday(birthday)
        if isvalid:
            self.book.add_birthday(new_record)
        return message

    @input_error
    def show_birthday(self, args):
        name = args[0]
        return self.book.show_birthday(name)

    def get_next_week_birthdays(self):
        return self.book.get_next_week_birthdays()

    def get_birthdays_for_amount_days(self, args):
        days = args[0]
        return self.book.get_birthdays_for_amount_days(days)

    @input_error
    def add_contact_email(self, args):
        name, email = args
        return self.book.add_email(name, email)

    @input_error
    def change_contact_email(self, args):
        name, old_email, new_email = args
        return self.book.change_email(name, old_email, new_email)

    @input_error
    def get_contact_email(self, args):
        name = args[0]
        return self.book.get_email(name)

    @input_error
    def add_contact_address(self, args):
        name, *address_parts = args
        address = " ".join(address_parts)
        return self.book.add_address(name, address)

    @input_error
    def change_contact_address(self, args, new_address):
        name, *address_parts = args
        old_address = " ".join(address_parts)
        return self.book.change_address(name, old_address, new_address)

    @input_error
    def get_contact_address(self, args):
        name = args[0]
        return self.book.get_address(name)

    def generate_random_book(self):
        self.book.generate_random_data()
        return self.get_all_contacts()

    @input_error
    def add_note(self, value):
        # TODO add validation of presence
        return self.note_book.add_note(Note(value))

    @input_error
    def find_notes(self, keyword):
        return self.note_book.find_notes(keyword)

    @input_error
    def edit_note(self, index, new_note):
        index = int(index)
        return self.note_book.edit_note(index, new_note)

    @input_error
    def delete_note(self, index):
        index = int(index)
        return self.note_book.delete_note(int(index))

    def all_notes(self):
        return str(self.note_book)

    def save_to_json(self):
        with open("result.json", "w") as fh:
            json.dump(self.book.to_dict(), fh)
        return "Storing is done"

    def load_from_json(self):
        with open("result.json", "r") as fh:
            json_data = json.load(fh)
            self.book = AddressBook.from_dict(json_data)
        return "Restoring is done"
