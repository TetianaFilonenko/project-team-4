"""Module providing classes and functions for working with notes"""

from collections import UserList
import json
import os
import random
from importlib import resources


class Note:
    """Represents a single note, which is a textual content tagged with keywords."""

    def __init__(self, value: str, tags=None):
        """
        Initializes a new Note instance.
        """
        self.value = value
        self.tags = tags

    def __str__(self):
        if self.tags and len(self.tags) > 0:
            return f"{self.value} - Tags: {', '.join(self.tags)}"
        else:
            return f"{self.value}"

    def add_tag(self, tag: str):
        """
        Adds a tag to the note.
        """
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        """
        Removes a tag to the note.
        """
        self.tags.discard(tag)

    def has_tag(self, partial_tag: str):
        """
        Checks if any of the note's tags contain the given partial tag as a substring.
        Example:
            If the note has tags ['workshop', 'homework'], calling has_tag('work') will return True.

        """
        return any(partial_tag in tag for tag in self.tags)

    @property
    def value(self):
        """Value getter."""
        return self.__value

    @value.setter
    def value(self, new_value):
        """Value setter."""
        if new_value.strip() == "":
            raise ValueError("New value cannot be None or empty")
        self.__value = new_value.replace("\\n", "\n")

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

        return "\n".join(
            f"{index + 1}: {note}" for index, note in enumerate(found_notes)
        )

    def find_notes_by_tag(self, tag: str):
        """Function to find notes containing a specific tag."""
        found_notes = []
        for note in self.data:
            if note.has_tag(tag):
                found_notes.append(note)

        return "\n".join(
            f"{index + 1}: {note}" for index, note in enumerate(found_notes)
        )

    def sort_notes_by_tag(self, tag):
        """
        Sorts the notes in the notebook based on whether they contain the specified tag.
        Notes with the specified tag are ordered to appear first.
        """
        return sorted(self.data, key=lambda note: tag in note.tags)

    def edit_note(self, index: int, new_value: str, new_tags: str, mode):
        """Function to edit a note at a specific index."""

        if 0 <= index < len(self.data):
            if not mode == "skip_description":
                self.data[index].value = new_value
            if not mode == "skip_tags":
                new_tags = new_tags.split(",")
                self.data[index].tags = new_tags
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
        Parameters:
            save (bool): If True, the generated note is added to the notebook.
        Note:
            The source of quotes is a text file named 'quotes.txt' located in the 'console_bot' package resources.
        """
        with resources.open_text("console_bot", "quotes.txt") as file:
            poems = file.readlines()
        poem = random.choice(poems).strip()  # Randomly select a poem from the list
        note = Note(poem)
        if save:
            self.add_note(note)
        return note.value

    def __str__(self):
        """Convert notebook to string."""
        return "\n".join(f"{index + 1}: {note}" for index, note in enumerate(self.data))

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
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            return cls.from_list(data)
        else:
            return cls()

    def save_to_file(self, filename: str = "note_book.json"):
        """
        Save notebook to file.
        """
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_list(), file, ensure_ascii=False)
