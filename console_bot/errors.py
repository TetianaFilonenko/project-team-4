class DuplicateError(BaseException):
    """Contact has been already added"""
class NotFoundError(BaseException):
    """Contact has not been found"""

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "No argument for contact name was provided"
        except KeyError:
            return "Name can't be found in contacts"
        except DuplicateError:
            return "Contact was not added. Same contact was added before. You can use change command"
        except NotFoundError:
            return f"Contact with name is not present in our system"

    return inner
