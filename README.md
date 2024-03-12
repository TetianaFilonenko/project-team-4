Final version of the bot
Main functions:
- has helper methods 
  - 'help' to show all commands
  - 'close' closes current session of bot
  - 'hello'shows welcome message
- can add, change phones for each contact
- can add/show birthday for each contact
- can show birthdays list for the contacts that celebrating birthday next week
- can generate fake contacts
- can save/restore contacts in json format

```
Example of usage

Welcome to the assistant bot!
Enter a command: help
Available commands:
  hello                          - Ask the bot how it can help you.
  add [name] [phone]             - Adds a contact with the specified name and phone number.
  change [name] [phone]          - Changes the phone number for the specified contact.
  phone [name]                   - Retrieves the phone number for the specified contact.
  all                            - Displays all contacts in the system.
  help                           - Shows this help message.
  add-birthday [name] [birthday] - Adds birthday to the contact
  show-birthday [name]           - Shows birthday for specific contact
  birthdays                      - Shows birthdays for all contacts celebrating next week
  close/exit                     - Exits the program.
  save                           - Store current book to json file with name result.json
  restore                        - Restore book from result.json
  random-book                    - generate random book with 10 contacts

Enter a command: random-book

Enter a command: random-book
Contact name: Christopher, phones: 0107307566; birthday: November 21st
Contact name: Lawrence, phones: 0460934055; birthday: March 28th
Contact name: Aaron, phones: 2715574547; birthday: November 25th
Contact name: Laura, phones: 1006038096; birthday: April 19th
Contact name: Pamela, phones: 3999439617; birthday: September 3rd
Contact name: Melissa, phones: 2656779575; birthday: December 24th
Contact name: James, phones: 6442366334; birthday: July 14th
Contact name: Johnny, phones: 4257113745; birthday: June 8th
Contact name: Joshua, phones: 1112043689; birthday: July 21st
Contact name: Nicole, phones: 1471306153; birthday: May 6th
Enter a command: add Nicole 1111111111
phone: 1111111111 was added to record Nicole
Enter a command: add-birthday John 05.03.2001
birthday: 05.03.2001 was added to record John
Enter a command: add Tetiana 1234554321
phone: 1234554321 was added to record Tetiana
Enter a command: add-birthday Melissa 08.03.1999
birthday: 08.03.1999 was added to record Melissa
Contact name: Christopher, phones: 0107307566; birthday: November 21st
Contact name: Lawrence, phones: 0460934055; birthday: March 28th
Contact name: Aaron, phones: 2715574547; birthday: November 25th
Contact name: Laura, phones: 1006038096; birthday: April 19th
Contact name: Pamela, phones: 3999439617; birthday: September 3rd
Contact name: Melissa, phones: 2656779575; birthday: March 8th
Contact name: James, phones: 6442366334; birthday: July 14th
Contact name: Johnny, phones: 4257113745; birthday: June 8th
Contact name: Joshua, phones: 1112043689; birthday: July 21st
Contact name: Nicole, phones: 1111111111, 1471306153; birthday: May 6th
Contact name: John, birthday: March 5th
Contact name: Tetiana, phones: 1234554321;
Enter a command: birthdays
Tuesday: John
Friday: Melissa
Enter a command: save
Storing is done
