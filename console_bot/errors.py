"""Module providing functions for working with Error"""


def input_error(func):
    """
    Decorator function to handle errors in the input.
    """

    def inner(*args, **kwargs):
        """
        Inner function to handle errors in the input.
        """
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input. Please provide valid arguments."
        except IndexError:
            return "Index out of range."
        except KeyError:
            return "Name can't be found in contacts"

    return inner
