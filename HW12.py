from Clase import AddressBook, Record, Name, Phone, Birthday

contacts = AddressBook()

def input_error(func):
    
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Print help"
        except KeyError:
            return 'Contact not found, try again or use help'
        except AttributeError:
            return 'Not enough params. Print help'
    return inner

@input_error
def add(*args):
    list_of_param = args[0].split()
    name = list_of_param[0]
    birthday = None
    phone_numbers = []
    for param in list_of_param[1:]:
        if len(param) == 12 and param.isnumeric():
            phone_numbers.append(Phone(param))
        else:
            birthday = Birthday(param)

    record = Record(Name(name), phone_numbers, birthday)
    contacts.add_record(record)

    if not birthday:
        return f'{name}, {phone_numbers[0]}'
    return f'{name},{phone_numbers[0]},{birthday}'

def show_all(*args, contacts=contacts):
    if not contacts.data:
        return "No contacts"
    
    contact_list = []
    for name, record in contacts.data.items():
        phones = ', '.join(str(phone) for phone in record.phone)
        if record.birthday:
            contact_list.append(f'{name} {phones} days to birthday: {record.days_to_birthday()}')
        else:
            contact_list.append(f'{name} {phones}, Date of birth is not specified')

    page = args[0]

    if not page:
        return "\n".join(contact_list)
    
    for records in contacts.iterator(int(page)):
        for name, record in records:
            phones = ', '.join(str(phone) for phone in record.phone)
            days_to_birthday = f"days to birthday: {record.days_to_birthday()}" if record.birthday else ""
            print(f"{name} {phones} {days_to_birthday}")
        print('*' * 100)
    
@input_error
def phone(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone_number = [Phone(phone) for phone in list_of_param[1:-1]]
    record = contacts.get(name.value)
    phone_number = record.phone[0]
    return f'{phone_number}'

@input_error
def change(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone_number = [Phone(phone) for phone in list_of_param[1:]]
    record = contacts.get(name.value)
    if not record:
        raise KeyError
    if not phone_number:
        raise AttributeError
    record.phone = phone_number
    return f'Contact {name.value} updated {str(phone_number[0])}'

def exit(*args):
    return "Good bye!"

def no_command(*args):
    return 'Unknown command, try again or help'

def help(*args):
    return """
"hello"                     >>> "How can I help you?"
"add"                       >>> "Example add name phone birthday" "add Alex 380996655789 12.12.2012"
"change"                    >>> "Example change name new phone number"
"phone"                     >>> "Example phone name" "phone Alex"
"show all"                  >>> "Show all saved name phone birthday"
"good bye", "close", "exit" >>> "End of program" 
"""

def hello(*args):
    return "How can I help you?"

COMMANDS = {help: 'help',
            hello: 'hello',
            add: 'add',
            show_all: 'show all',
            phone: 'phone',
            change: 'change',
            exit: 'exit'
            }

def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
    return no_command, None

def main():
    print('Hello user! enter help for instructions')
    print(contacts.load_from_file('contacts.bin'))
    while True:

        user_input = input('>>>')
        
        if user_input in ('good bye', 'close', 'exit'):
            print(contacts.save_to_file('contacts.bin'))
            print(exit())
            break 

        command, data = command_handler(user_input)
        print(command(data))    

if __name__ == '__main__':
    
    main()