from .input_manager import InputManager


def get_index(field, len):
    """
    Function to get index from user
    """
    index = input(f"Enter a index of {field}(eg. 1 for first): ")
    if index.isnumeric():
        index = int(index)
    else:
        index = 0
    if index > len or not index:
        print("Invalid index, error executing edit command, try again")
        index = 0
    return index


def edit_field(input_manager, args, field, get_func, put_func):
    """
    Function to update/delete phone/email/address
    """
    name = args[0]
    record = input_manager.book[name]
    if field in ("phone", "email"):
        fields = field + "s"
    else:
        fields = field + "es"
    print(get_func(args))
    if not getattr(record, fields):
        return None  # continue
    index = get_index(field, len(getattr(record, fields)))
    if not index:
        return None  # continue
    nvalue = input(f"Enter new {field} or enter 'delete': ")
    if nvalue == "delete":
        input_manager.delete_field(name, field, index - 1)
        print(f"{field} has been deleted")
    else:
        if field == "address":
            print(put_func([name, str(getattr(record, fields)[index - 1])], nvalue))
        else:
            print(put_func([name, str(getattr(record, fields)[index - 1]), nvalue])) 


def edit_record(input_manager, args):
    """
    Function to handle update/delete phone/email/address from user input
    """
    if len(args) < 2:
        print("Invalid input, expected 'edit field recordname'")
        return None  # continue
    field = args[0]
    args.pop(0)

    if not input_manager.get_contact_phone(args):
        print(f"{args[0]} not found")
        return None  # continue

    if field == "phone":
        get_func = input_manager.get_contact_phone
        put_func = input_manager.change_contact

    elif field == "email":
        get_func = input_manager.get_contact_email
        put_func = input_manager.change_contact_email

    elif field == "address":
        get_func = input_manager.get_contact_address
        put_func = input_manager.change_contact_address    
    
    else:
        print("not supported field")
        return None  # continue
    
    edit_field(input_manager, args, field, get_func, put_func)