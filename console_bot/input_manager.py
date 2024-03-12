from .errors import input_error
from .address_book import Record, AddressBook
import json

class InputManager:
    def __init__(self):
        self.book = AddressBook()

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
        name, new_phone = args
        new_record = Record(name)
        isvalid, message = new_record.add_phone(new_phone)
        if isvalid:
            self.book.add_contact(new_record, override=True)
        return message

    @input_error
    def get_contact_phone(self, args):
        name = args[0]
        return self.book.find(name)

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

    def generate_random_book(self):
        self.book.generate_random_data()
        return self.get_all_contacts()


    def save_to_json(self):
        with open('result.json', "w") as fh:
            json.dump(self.book.to_dict(), fh)
        return "Storing is done"

    def load_from_json(self):
        with open('result.json', 'r') as fh:
            json_data = json.load(fh)
            self.book = AddressBook.from_dict(json_data)
        return "Restoring is done"

