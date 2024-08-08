from pydantic import ValidationError

from address import Address
import sqlite3

conn = sqlite3.connect('addresses.sqlite3')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS addresses (lastname TEXT, firstname TEXT, street TEXT, number TEXT, zip_code INTEGER, city TEXT, birthdate TEXT, phone TEXT, email TEXT)")
conn.commit()

if __name__ == "__main__":
    address = Address("Doe", "John", "Main Street", 123, 12345,
                      "Springfield", "01.01.1970", "+49123456789", "john.doe@doe-mail.io")
    print(address)
    print(repr(address))

