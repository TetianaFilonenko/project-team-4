def input_error(func):
    # FIXME: message here are too specific
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input. Please provide valid arguments."
        except IndexError:
            return "Index out of range."
        except KeyError:
            return "Name can't be found in contacts"

    return inner
