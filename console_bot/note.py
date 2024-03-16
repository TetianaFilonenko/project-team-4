"""Module providing classes and functions for working with notes"""

from collections import UserList
import json
import os

class Note:
    """Class representing a note"""

    def __init__(self, value, tags=None):
        self.value = value
        self.tags = set(tags) if tags else set()


    def __str__(self):
        return f"{self.value} - Tags: {', '.join(self.tags)}"

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.discard(tag)

    def has_tag(self, tag):
        return tag in self.tags

    @property
    def value(self):
        """Value getter."""
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value.strip() == "":
            raise ValueError("New value cannot be None or empty")
        self.__value = new_value

    def to_dict(self):
        """Convert note to dictionary."""
        return {"value": self.value}


class NoteBook(UserList):
    """Class representing a notebook - list of notes"""

    def __init__(self):
        super().__init__()

    def add_note(self, note: Note):
        """Function adding note to notebook."""
        self.data.append(note)
        return "Note was added"

    def find_notes(self, keyword):
        """Function to find notes containing a specific keyword."""
        found_notes = []
        for note in self.data:
            if keyword in note.value:
                found_notes.append(note)

        return "\n".join(f"{index}: {note}" for index, note in enumerate(found_notes))

    def edit_note(self, index, new_value):
        """Function to edit a note at a specific index."""
        if 0 <= index < len(self.data):
            self.data[index].value = new_value
            return "Note was changed"
        else:
            raise IndexError("Index out of range")

    def delete_note(self, index):
        """Function to delete a note at a specific index."""
        if 0 <= index < len(self.data):
            del self.data[index]
            return "Note was deleted"
        else:
            raise IndexError("Index out of range.")

    def find_notes_by_tag(self, tag):
        return [note for note in self.data if note.has_tag(tag)]

    def sort_notes_by_tag(self, tag):
        return sorted(self.data, key=lambda note: tag in note.tags)

    def __str__(self):
        """Convert notebook to string."""
        return "\n".join(f"{index}: {note}" for index, note in enumerate(self.data))
    
    def to_dict(self):
        """Convert notebook to a list of dictionaries."""
        return [note.to_dict() for note in self.data]

    def to_list(self):
        """Convert notebook to a list of dictionaries."""
        return [note.to_dict() for note in self.data]

    @classmethod
    def from_list(cls, data):
        note_book = cls()
        for el in data:
            note = Note(el["value"])
            note_book.data.append(note)
        return note_book


    @classmethod
    def load_from_file(cls, filename="note_book.json"):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
            return cls.from_list(data)
        else:
            return cls()

    def save_to_file(self, filename='note_book.json'):
        with open(filename, 'w') as file:
            json.dump(self.to_list(), file)
