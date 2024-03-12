from collections import UserDict
import re
from faker import Faker
from datetime import datetime
from .birthdays_per_week import get_birthdays_per_week

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def to_dict(self):
        return str(self.value)

class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime.strptime(new_value, '%d.%m.%Y')
        except ValueError:
            self.__value = None

    def is_valid(self):
        return bool(self.__value)

    def ordinal(self):
        day = self.__value.day
        return "%d%s" % (day, "th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th"))

    def to_dict(self):
        return self.__value.strftime('%d.%m.%Y')

    def __str__(self):
        return self.__value.strftime(f'%B {self.ordinal()}')


class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if re.search(r"^[0-9]{10}$", new_value) and len(new_value) == 10:
            self.__value = new_value
        else:
            self.__value = None

    def is_valid(self):
        return bool(self.__value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.birthday = None
        self.phones = []


    def add_phone(self, phone: str):
        phone_instance = Phone(phone)
        if phone_instance.is_valid():
            self.phones.append(phone_instance)
            return phone_instance.is_valid(), f'phone: {phone} was added to record {self.name.value}'
        else:
            return phone_instance.is_valid(), f'Only 10-digits numbers are accepted, you entered: {phone}'

    def remove_phone(self, phone):
        if isinstance(phone, Phone):
            phone = phone.value
        self.phones = [el for el in self.phones if el.value != phone]


    def edit_phone(self, old_phone, new_phone):
        if isinstance(old_phone, Phone) and isinstance(new_phone, Phone):
            old_phone = old_phone.value
            new_phone = new_phone.value

        self.phones = [Phone(new_phone) if el.value == old_phone else el for el in self.phones ]

    def find_phone(self, phone):
        if isinstance(phone, Phone):
            phone = phone.value
        for _i in filter(lambda el: phone == el.value, self.phones):
            return f"{self.name} has {phone} in phone list\n{str(self)}"
        return f"{self.name} doen't have {phone} in phone list\n{str(self)}"

    def add_birthday(self, birthday):
        birthday_instance = Birthday(birthday)
        if birthday_instance.is_valid():
            self.birthday = birthday_instance
            return birthday_instance.is_valid(), f'birthday: {birthday} was added to record {self.name.value}'
        else:
            return birthday_instance.is_valid(), f"Only '%d.%m.%Y' date format is accepted, you entered: {birthday}"

    def __str__(self):
        if len(self.phones) > 0 and self.birthday:
            return f"Contact name: {self.name}, phones: {', '.join(p.value for p in self.phones)}; birthday: {self.birthday}"
        elif len(self.phones) > 0:
            return f"Contact name: {self.name}, phones: {', '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name}, birthday: {self.birthday}"

    def to_dict(self):
        return {
            "name": self.name.to_dict(),
            "birthday": self.birthday.to_dict() if self.birthday else '',
            "phones": [phone.to_dict() for phone in self.phones]
        }

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def find(self, name: str):
        for key, value in filter(lambda el: name == el[0], self.items()):
            return f"Found record with name: '{key}'. \nResult: {str(value)}"

    def add_contact(self, record: Record, override = False):
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

    def add_birthday(self, record: Record):
        if record.name.value in self.data.keys():
            # keep track of previous phone data
            record.phones = self.data[record.name.value].phones
            self.data[record.name.value] = record
        else:
            self.data[record.name.value] = record
        return record

    def show_birthday(self, name):
        if name not in self.data.keys():
            return f"Record with name {name} is not found"
        elif self.data[name].birthday:
            return self.data[name].birthday.value
        else:
            return f"Birthday data for Record with name {name} is not provided"

    def get_next_week_birthdays(self):
        result = [{"name": key, "birthday": value.birthday.value} for key, value in self.items() if value and value.birthday]

        return get_birthdays_per_week(result)

    def delete(self, name: str):
        del self.data[name]

    def generate_random_data(self):
        fake = Faker()
        for _i in range(0, 10):
            name = fake.first_name()
            phone_number = fake.numerify('##########')
            birthday = fake.date_object().strftime('%d.%m.%Y')

            record = Record(name)
            record.birthday = Birthday(birthday)
            record.phones.append(Phone(phone_number))

            self.data[name] = record

    def to_dict(self):
        return {key: value.to_dict() for key, value in self.data.items()}

    @classmethod
    def from_dict(cls, dict_data):
        address_book = cls()
        for record_name, record_data in dict_data.items():
            record = Record(record_data['name'])
            if len(record_data['birthday']) > 0:
                record.birthday = Birthday(record_data['birthday'])
            record.phones = [Phone(phone) for phone in record_data['phones']]
            address_book[record_name] = record
        return address_book
