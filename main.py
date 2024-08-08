from pydantic import ValidationError

from address import Address

if __name__ == "__main__":
    address = Address("Doe", "John", "Main Street", 123, 12345,
                      "Springfield", "01.01.1970", "+49123456789", "john.doe@doe-mail.io")
    print(address)
    print(repr(address))

