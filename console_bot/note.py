"""Module providing classes and functions for working with notes"""

from collections import UserList
import json
import os
import random
from importlib import resources


class Note:
    """Class representing a note"""

    def __init__(self, value: str, tags=[]):
        self.value = value
        self.tags = tags

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
        """Value setter."""
        if new_value.strip() == "":
            raise ValueError("New value cannot be None or empty")
        self.__value = new_value

    def to_dict(self):
        """Convert note to dictionary."""
        return {"value": self.value, "tags": self.tags}


class NoteBook(UserList):
    """Class representing a notebook - list of notes"""

    def __init__(self):
        super().__init__()

    def add_note(self, note: Note):
        """Function adding note to notebook."""
        self.data.append(note)
        return "Note was added"

    def find_notes(self, keyword: str):
        """Function to find notes containing a specific keyword."""
        found_notes = []
        for note in self.data:
            if keyword in note.value:
                found_notes.append(note)

        return "\n".join(f"{index}: {note}" for index, note in enumerate(found_notes))
    
    def find_notes_by_tag(self, tag):
        """Function to find notes containing a specific tag."""
        found_notes = []
        for note in self.data:
            if note.has_tag(tag):
                found_notes.append(note)

        return "\n".join(f"{index}: {note}" for index, note in enumerate(found_notes))
       
    def sort_notes_by_tag(self, tag):
        return sorted(self.data, key=lambda note: tag in note.tags)

    def edit_note(self, index: int, new_value: str):
        """Function to edit a note at a specific index."""
        if 0 <= index < len(self.data):
            self.data[index].value = new_value
            return "Note was changed"
        else:
            raise IndexError("Index out of range")

    def delete_note(self, index: int):
        """Function to delete a note at a specific index."""
        if 0 <= index < len(self.data):
            del self.data[index]
            return "Note was deleted"
        else:
            raise IndexError("Index out of range.")

    def generate_random(self, save=True):
        """
        Generate a random note and add it to the notebook.
        """
        with resources.open_text('console_bot', 'quotes.txt') as file:
            poems = file.readlines()
        poem = random.choice(poems).strip()  # Randomly select a poem from the list
        note = Note(poem)
        if save:
            self.add_note(note)
        return note.value

    def find_notes_by_tag(self, tag):
        return [note for note in self.data if note.has_tag(tag)]

    def sort_notes_by_tag(self, tag):
        return sorted(self.data, key=lambda note: tag in note.tags)

    def __str__(self):
        """Convert notebook to string."""
        return "\n".join(f"{index}: {note}" for index, note in enumerate(sorted(self.data, key=lambda x: x.value)))

    def to_list(self):
        """Convert notebook to a list of dictionaries."""
        return [note.to_dict() for note in self.data]

    @classmethod
    def from_list(cls, data: list[dict]):
        """
        Create notebook from a list of dictionaries.
        """
        note_book = cls()
        for el in data:
            note = Note(el["value"], el["tags"])
            note_book.data.append(note)
        return note_book

    @classmethod
    def load_from_file(cls, filename: str = "note_book.json"):
        """
        Load notebook from file.
        """
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
            return cls.from_list(data)
        else:
            return cls()

    def save_to_file(self, filename: str = 'note_book.json'):
        """
        Save notebook to file.
        """
        with open(filename, 'w') as file:
            json.dump(self.to_list(), file)
