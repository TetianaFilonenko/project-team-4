from .input_manager import InputManager


def get_index(field, len):
    index = input(f"Enter a index of {field}(eg. 1 for first): ")
    if index.isnumeric():
        index = int(index)
    else:
        index = 0
    if index > len or not index:
        print("Invalid index, error executing edit command, try again")
        index = 0
    return index


def edit_record(args):
    input_manager = InputManager()
    if len(args) < 2:
        print("Invalid input, expected 'edit field recordname'")
        return None  # continue
    field = args[0]
    args.pop(0)

    if not input_manager.get_contact_phone(args):
        print(f"{args[0]} not found")
        return None  # continue

    record = input_manager.book[args[0]]

    if field == "phone":
        print(input_manager.get_contact_phone(args))
        if not record.phones:
            return None  # continue
        index = get_index("phone", len(record.phones))
        if not index:
            return None  # continue
        nphone = input("Enter new phone or enter 'delete': ")
        if nphone == "delete":
            input_manager.delete_field(args[0], "phone", index - 1)
            print("phone has been deleted")
        else:
            print(
                input_manager.change_contact(
                    [args[0], str(record.phones[index - 1]), nphone]
                )
            )

    elif field == "email":
        print(input_manager.get_contact_email(args))
        if not record.emails:
            return None  # continue
        index = get_index("email", len(record.emails))
        if not index:
            return None  # continue
        nemail = input("Enter new email or enter 'delete': ")
        if nemail == "delete":
            input_manager.delete_field(args[0], "email", index - 1)
            print("email has been deleted")
        else:
            print(
                input_manager.change_contact_email(
                    [args[0], str(record.emails[index - 1]), nemail]
                )
            )

    elif field == "address":
        print(input_manager.get_contact_address(args))
        if not record.addresses:
            return None  # continue
        index = get_index("address", len(record.addresses))
        if not index:
            return None  # continue
        naddr = input("Enter new address or enter 'delete': ")
        if naddr == "delete":
            input_manager.delete_field(args[0], "address", index - 1)
            print("address has been deleted")
        else:
            print(
                input_manager.change_contact_address(
                    [args[0], str(record.addresses[index - 1])], naddr
                )
            )
    else:
        print("not supported field")
