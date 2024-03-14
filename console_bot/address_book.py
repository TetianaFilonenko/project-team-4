"""Module providing classes and functions for working with AddressBook"""

from collections import UserDict
import re
from datetime import datetime
import json
import os
from faker import Faker
from .birthdays_per_week import (
    get_birthdays_per_week,
    get_birthdays_in_next_days,
    get_today_birthday,
)


class Field:
    """
    Base class for all fields
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

    def to_dict(self):
        """
        Convert the value of the object to a dictionary.
        """
        return str(self.value)


class Birthday(Field):
    """
    Class representing a birthday field
    """

    @property
    def value(self):
        """
        Property method to access the value attribute of the object.
        """
        return self.__value

    @value.setter
    def value(self, new_value: str):
        try:
            self.__value = datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            self.__value = None

    def is_valid(self):
        """
        Check if birthday is valid
        """
        return bool(self.__value)

    def ordinal(self):
        """
        Return a string with the ordinal number for the day
        """
        day = self.__value.day
        return "%d%s" % (
            day,
            (
                "th"
                if 4 <= day % 100 <= 20
                else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            ),
        )

    def to_dict(self):
        return self.__value.strftime("%d.%m.%Y")

    def __str__(self):
        return self.__value.strftime(f"%B {self.ordinal()}")


class Name(Field):
    """
    Class representing a name field
    """


class Phone(Field):
    """
    Class representing a phone field
    """

    @property
    def value(self):
        """
        Property method to access the value attribute of the object.
        """
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """
        Setter for phone number checking if it's valid 10-digits number
        """
        if re.search(r"^[0-9]{10}$", new_value) and len(new_value) == 10:
            self.__value = new_value
        else:
            self.__value = None

    def is_valid(self):
        """
        Check if the value of the field is valid.
        """
        return bool(self.__value)


class Email(Field):
    """
    Class representing an email field
    """

    @property
    def value(self):
        """
        Property method to access the value attribute of the object.
        """
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """
        Setter for email checking if it's valid email via regex
        """
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_value):
            self.__value = new_value
        else:
            self.__value = None

    def is_valid(self):
        """
        Check if the value of the field is valid.
        """
        return bool(self.__value)


class Address(Field):
    """
    Class representing an address field
    """

    @property
    def value(self):
        """
        Property method to access the value attribute of the object.
        """
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Setter for address checking if it's valid address which is not empty string
        """
        if isinstance(new_value, str) and len(new_value) > 0:
            self.__value = new_value
        else:
            self.__value = None

    def is_valid(self):
        """
        Check if the value of the field is valid.
        """
        return bool(self.__value)


class Record:
    """
    Class representing a record in the address book
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.birthday = None
        self.phones = []
        self.emails = []
        self.addresses = []

    def add_phone(self, phone: str):
        """
        Add phone to the record. Check if it's valid and return message

        """
        phone_instance = Phone(phone)
        if phone_instance.is_valid():
            self.phones.append(phone_instance)
            return (
                phone_instance.is_valid(),
                f"phone: {phone} was added to record {self.name.value}",
            )
        else:
            return (
                phone_instance.is_valid(),
                f"Only 10-digits numbers are accepted, you entered: {phone}",
            )

    def remove_phone(self, phone: str):
        """
        Remove phone from the record
        """
        if isinstance(phone, Phone):
            phone = phone.value
        self.phones = [el for el in self.phones if el.value != phone]

    def edit_phone(self, old_phone_value: str, new_phone_value: str):
        """
        Edit phone in the record. Check if old and new phone are valid and return message
        """
        old_phone = Phone(old_phone_value)
        new_phone = Phone(new_phone_value)
        if new_phone.is_valid() and old_phone.is_valid():
            self.phones = [
                new_phone if el.value == old_phone_value else el for el in self.phones
            ]
            return (
                True,
                f"Phone: {old_phone_value} was changed to {new_phone_value} for record {self.name.value}",
            )
        else:
            return (
                False,
                f"Invalid phone format. Old: {old_phone_value}, New: {new_phone_value}",
            )

    def find_phone(self, phone: str):
        """
        Find phone in the record. Return message if found or not found
        """
        if isinstance(phone, Phone):
            phone = phone.value
        for _i in filter(lambda el: phone == el.value, self.phones):
            return f"{self.name} has {phone} in phone list\n{str(self)}"
        return f"{self.name} doesn't have {phone} in phone list\n{str(self)}"

    def add_birthday(self, birthday: str):
        """
        Add birthday to the record. Check if it's valid and return message
        """
        birthday_instance = Birthday(birthday)
        if birthday_instance.is_valid():
            self.birthday = birthday_instance
            return (
                birthday_instance.is_valid(),
                f"birthday: {birthday} was added to record {self.name.value}",
            )
        else:
            return (
                birthday_instance.is_valid(),
                f"Only '%d.%m.%Y' date format is accepted, you entered: {birthday}",
            )

    def add_email(self, email: str):
        """
        Add email to the record. Check if it's valid and return message
        """
        email_instance = Email(email)
        if email_instance.is_valid():
            self.emails.append(email_instance)
            return True, f"Email: {email} was added to record {self.name.value}"
        else:
            return False, f"Invalid email format: {email}"

    def remove_email(self, email: str):
        """
        Remove email from the record
        """
        self.emails = [el for el in self.emails if el.value != email]

    def edit_email(self, old_email_value: str, new_email_value: str):
        """
        Edit email in the record. Check if old and new email are valid and return message
        """
        old_email = Email(old_email_value)
        new_email = Email(new_email_value)
        if new_email.is_valid() and old_email.is_valid():
            self.emails = [
                new_email if el.value == old_email_value else el for el in self.emails
            ]
            return (
                True,
                f"Email: {old_email_value} was changed to {new_email_value} for record {self.name.value}",
            )
        else:
            return (
                False,
                f"Invalid email format. Old: {old_email_value}, New: {new_email_value}",
            )

    def add_address(self, address: str):
        """
        Add address to the record. Check if it's valid and return message
        """
        address_instance = Address(address)
        if address_instance.is_valid():
            self.addresses.append(address_instance)
            return True, f"Address: {address} was added to record {self.name.value}"
        else:
            return False, f"Invalid address format: {address}"

    def remove_address(self, address: str):
        """
        Remove address from the record
        """
        self.addresses = [el for el in self.addresses if el.value != address]

    def edit_address(self, old_address_value: str, new_address_value: str):
        """
        Edit address in the record. Check if old and new address are valid and return message
        """
        old_address = Address(old_address_value)
        new_address = Address(new_address_value)
        if new_address.is_valid() and old_address.is_valid():
            self.addresses = [
                new_address if el.value == old_address_value else el
                for el in self.addresses
            ]
            return (
                True,
                f"Address: {old_address_value} was changed to {new_address_value} for record {self.name.value}",
            )
        else:
            return (
                False,
                f"Invalid address format. Old: {old_address_value}, New: {new_address_value}",
            )

    def __str__(self):
        """
        Return string representation of the record. If field is empty, it's not shown
        """
        parts = [f"Contact name: {self.name}"]
        if self.phones:
            parts.append(f"phones: {', '.join(p.value for p in self.phones)}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        if self.emails:
            parts.append(f"emails: {', '.join(e.value for e in self.emails)}")
        if self.addresses:
            parts.append(f"addresses: {', '.join(a.value for a in self.addresses)}")
        return "; ".join(parts)

    def to_dict(self):
        """
        Convert record to dictionary by converting all fields to dictionaries
        """
        return {
            "name": self.name.to_dict(),
            "birthday": self.birthday.to_dict() if self.birthday else "",
            "phones": [phone.to_dict() for phone in self.phones],
            "emails": [email.to_dict() for email in self.emails],
            "addresses": [address.to_dict() for address in self.addresses],
        }


class AddressBook(UserDict):
    """
    Class representing an address book
    """

    def find(self, name: str):
        """
        Find record by name. Return message if found.
        """
        for key, value in filter(lambda el: name == el[0], self.items()):
            return f"Found record with name: '{key}'. \nResult: {str(value)}"

    def find_all(self, term: str):
        """
        Find all records containing term in any field. Return message if found.
        """
        res = ""
        res1 = self.find(term)
        if not res1:
            res1 = "\nNot found in names"
        else:
            res1 = "\n" + res1
        for value in filter(
                lambda el: re.search(term, str(el))
                           and not re.search(str(el), res)
                           and not re.search(str(el), res1),
                self.values(),
        ):
            res = res + f"{str(value)}\n"
        if res:
            res = "\n-=Found in other fields=-\n" + res
        else:
            res = "\nNothing found in fields\n"
        return res1 + res

    def add_contact(self, record: Record, override=False):
        """
        Add contact to the address book. If override is True, it will override the existing contact
        """
        if override and record.name.value in self.data.keys():
            # keep track of previous birthday data
            record.birthday = self.data[record.name.value].birthday
            self.data[record.name.value] = record
        elif record.name.value in self.data.keys():
            record.phones += self.data[record.name.value].phones
            # keep track of previous birthday data
            record.birthday = self.data[record.name.value].birthday
            self.data[record.name.value] = record
        else:
            self.data[record.name.value] = record
        return record

    def change_contact(self, name: str, old_phone: str, new_phone: str):
        """
        Change phone in the contact. Return message if changed or not found
        """
        if name in self.data:
            _, message = self.data[name].edit_phone(old_phone, new_phone)
            return message
        else:
            return f"Contact {name} not found. Add it first to the contact book"

    def add_birthday(self, record: Record):
        """
        Add birthday to the contact. Return message if added or not found
        """
        if record.name.value in self.data.keys():
            # keep track of previous phone data
            record.phones = self.data[record.name.value].phones
            self.data[record.name.value] = record
        else:
            self.data[record.name.value] = record
        return record

    def show_birthday(self, name: str):
        """
        Show birthday for the contact. Return message if found or not found
        """
        if name not in self.data.keys():
            return f"Record with name {name} is not found"
        elif self.data[name].birthday:
            return self.data[name].birthday.value
        else:
            return f"Birthday data for Record with name {name} is not provided"

    def get_next_week_birthdays(self):
        """
        Get all birthdays for the next week via helper function.
        """
        result = [
            {"name": key, "birthday": value.birthday.value}
            for key, value in self.items()
            if value and value.birthday
        ]

        return get_birthdays_per_week(result)

    def get_birthdays_for_amount_days(self, days: int):
        """
        Get all birthdays for the next amount of days via helper function.
        """
        result = [
            {"name": key, "birthday": value.birthday.value}
            for key, value in self.items()
            if value and value.birthday
        ]

        return get_birthdays_in_next_days(result, days)

    def check_today_birthdays(self):
        """
        Get all birthdays for today via helper function.
        """
        result = [
            {"name": key, "birthday": value.birthday.value}
            for key, value in self.items()
            if value and value.birthday
        ]

        return get_today_birthday(result)

    def add_email(self, name: str, email: str):
        """
        Add email to the contact. Return message if added or not found
        """
        if name in self.data:
            _, message = self.data[name].add_email(email)
            return message
        else:
            return f"Contact {name} not found. Add it first to the contact book"

    def change_email(self, name: str, old_email: str, new_email: str):
        """
        Change email in the contact. Return message if changed or not found
        """
        if name in self.data:
            _, message = self.data[name].edit_email(old_email, new_email)
            return message
        else:
            return f"Contact {name} not found. Add it first to the contact book"

    def get_email(self, name: str):
        """
        Get email for the contact. Return message if found or not found
        """
        if name in self.data and self.data[name].emails:
            return ", ".join(email.value for email in self.data[name].emails)
        else:
            return f"Email for contact {name} not found or not set."

    def add_address(self, name: str, address: str):
        """
        Add address to the contact. Return message if added or not found
        """
        if name in self.data:
            _, message = self.data[name].add_address(address)
            return message
        else:
            return f"Contact {name} not found. Add it first to the contact book"

    def change_address(self, name: str, old_address: str, new_address: str):
        """
        Change address in the contact. Return message if changed or not found
        """
        if name in self.data:
            _, message = self.data[name].edit_address(old_address, new_address)
            return message
        else:
            return f"Contact {name} not found. Add it first to the contact book"

    def get_address(self, name: str):
        """
        Get address for the contact. Return message if found or not found
        """
        if name in self.data and self.data[name].addresses:
            return ", ".join(address.value for address in self.data[name].addresses)
        else:
            return f"Address for contact {name} not found or not set."

    def delete(self, name: str):
        """
        Delete contact from the address book.
        """
        del self.data[name]

    def generate_random_data(self):
        """
        Generate random data for the address book for testing purposes via Faker library
        """
        fake = Faker()
        for _i in range(0, 10):
            name = fake.first_name()
            phone_number = fake.numerify("##########")
            birthday = fake.date_object().strftime("%d.%m.%Y")

            record = Record(name)
            record.birthday = Birthday(birthday)
            record.phones.append(Phone(phone_number))

            self.data[name] = record

    def to_dict(self):
        """
        Convert the data dictionary to a nested dictionary.
        """
        return {key: value.to_dict() for key, value in self.data.items()}

    @classmethod
    def from_dict(cls, dict_data: dict):
        """
        Convert dictionary to address book by converting all records to Record objects
        """
        address_book = cls()
        for record_name, record_data in dict_data.items():
            record = Record(record_data["name"])
            if len(record_data["birthday"]) > 0:
                record.birthday = Birthday(record_data["birthday"])
            record.phones = [Phone(phone) for phone in record_data["phones"]]
            record.addresses = [
                Address(address) for address in record_data["addresses"]
            ]
            record.emails = [Email(email) for email in record_data["emails"]]
            address_book[record_name] = record
        return address_book

    @classmethod
    def load_from_file(cls, filename: str = "address_book.json"):
        """
        Load address book from file
        """
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
            return cls.from_dict(data)
        else:
            return cls()

    def save_to_file(self, filename: str = "address_book.json"):
        """
        Save address book to file
        """
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)
