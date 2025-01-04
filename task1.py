from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must be a number of length 10")
        super().__init__(value)

class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None:
        phone = phone.strip()
        if any(p.value == phone for p in self.phones):
            raise ValueError(f"Phone {phone} already exists in contacts")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone = phone.strip()
        self.phones = list(filter(lambda p: p.value != phone, self.phones))
        print(f"Phone {phone} successfully removed")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("New phone must be a number of length 10")
        if any(p.value == new_phone for p in self.phones):
            raise ValueError(f"Phone {new_phone} already exists in contacts")
        found_phone = self.find_phone(old_phone.strip())
        found_phone.value = new_phone
        print(f"New phone {new_phone} successfully replaced old phone {old_phone}")

    def find_phone(self, phone: str) -> Phone:
        phone = phone.strip()
        found_phone = next((p for p in self.phones if p.value == phone), None)
        if found_phone is None:
            raise Exception(f"Phone {phone} not found in contacts")
        return found_phone

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.last_id = 0

    def add_record(self, record: Record) -> None:
        self.last_id += 1
        self.data[self.last_id] = record

    def find(self, name: str) -> tuple[int, Record] | None:
        for key, record in self.data.items():
            if record.name.value == name:
                return key, record
        return None

    def delete(self, name: str):
        key = next((key for key in self.data.keys() if self.data[key].name.value == name), None)
        if key is None:
            print(f"Record with name {name} not found in contacts")
            return
        del self.data[key]
        print(f"Record {name} successfully deleted")



# Creating a new address book
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Create record for John
book.add_record(john_record)

# Create and add a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Output of all entries in the book
for name, record in book.data.items():
    print(record)

# Find and edit John's phone
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

# Search for a specific phone in a John record
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Output: 5555555555

# Deleting Jane's record
book.delete("Jane")