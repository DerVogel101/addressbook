import sqlite3
from contextlib import closing
from address import Address


def create_table():
    with closing(sqlite3.connect('addresses.sqlite3')) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastname TEXT,
                    firstname TEXT,
                    street TEXT,
                    number TEXT,
                    zip_code INTEGER,
                    city TEXT,
                    birthdate TEXT,
                    phone TEXT,
                    email TEXT,
                    UNIQUE(lastname, firstname, street, number, zip_code, city, birthdate)
                )
            ''')


def save_to_sqlite(addresses: list):
    ids = []
    with closing(sqlite3.connect('addresses.sqlite3')) as conn:
        cursor = conn.cursor()
        for address in addresses:
            try:
                cursor.execute('''
                    INSERT INTO addresses (lastname, firstname, street, number, zip_code, city, birthdate, phone, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (address.lastname, address.firstname, address.street, address.number, address.zip_code, address.city, address.birthdate, address.phone, address.email))
                ids.append(cursor.lastrowid)
            except sqlite3.IntegrityError:
                print(f"Duplicate entry found: {address}")
        conn.commit()
    return ids


if __name__ == "__main__":
    create_table()
    address = Address(lastname="ADoe", firstname="John", street="Main Street", number="123", zip_code=12345,
                      city="Springfield", birthdate="2000-01-01", phone="+49 176 1234 5678",
                      email="john.doe@doe-mail.io")
    ids = save_to_sqlite([address])
    print(f"Inserted IDs: {ids}")