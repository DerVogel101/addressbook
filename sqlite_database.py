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


class SqliteDatabase:
    def __init__(self, path: str):
        self.__path = path
        self.__conn = sqlite3.connect(path)

    def open(self):
        self.__conn = sqlite3.connect(self.__path)

    def close(self):
        self.__conn.close()

    def save(self):
        self.__conn.commit()

    def add(self, address_obj: Address) -> int:
        cursor = self.__conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO addresses (lastname, firstname, street, number, zip_code, city, birthdate, phone, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (address_obj.lastname, address_obj.firstname, address_obj.street, address_obj.number, address_obj.zip_code, address_obj.city, address_obj.birthdate, address_obj.phone, address_obj.email))
        except sqlite3.IntegrityError as e:
            print(f"Invalid entry found: {address_obj}\n"
                  f"{str(e)}")
        return cursor.lastrowid

    def get_where(self, where_clause: str) -> list[dict]:
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(f"SELECT * FROM addresses WHERE {where_clause}")
        result = cursor.fetchall()
        cursor.row_factory = None
        result = [dict(row) for row in result]
        return result

    def get_all(self) -> list[dict]:
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute('''
            SELECT * FROM addresses
        ''')
        result = cursor.fetchall()
        cursor.row_factory = None
        result = [dict(row) for row in result]
        return result

    def delete(self, row_id: int) -> int | None:
        cursor = self.__conn.cursor()
        cursor.execute('''
            DELETE FROM addresses WHERE id = ?
        ''', (row_id,))
        if cursor.rowcount == 1:
            return row_id
        else:
            return None

    def search(self, search_string: str) -> list[dict]:
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        query = """
            SELECT * FROM addresses WHERE
            lastname LIKE ? OR
            firstname LIKE ? OR
            street LIKE ? OR
            number LIKE ? OR
            zip_code LIKE ? OR
            city LIKE ? OR
            birthdate LIKE ? OR
            phone LIKE ? OR
            email LIKE ?
        """
        cursor.execute(query, [f'%{search_string}%'] * 9)
        result = cursor.fetchall()
        cursor.row_factory = None
        return [dict(row) for row in result]

    def update(self, row_id: int, **kwargs) -> int | None:
        previous = self.get_where(f"id = {row_id}")[0]
        previous.update(kwargs)
        cursor = self.__conn.cursor()
        cursor.execute('''
            UPDATE addresses SET
            lastname = ?,
            firstname = ?,
            street = ?,
            number = ?,
            zip_code = ?,
            city = ?,
            birthdate = ?,
            phone = ?,
            email = ?
            WHERE id = ?
        ''', (previous['lastname'], previous['firstname'], previous['street'], previous['number'], previous['zip_code'], previous['city'], previous['birthdate'], previous['phone'], previous['email'], row_id))
        if cursor.rowcount == 1:
            return row_id
        else:
            return None



if __name__ == "__main__":
    create_table()
    address = Address(lastname="ADoe", firstname="John", street="Main Street", number="123", zip_code=12345,
                      city="Springfield", birthdate="2000-01-01", phone="+49 176 1234 5678",
                      email="john.doe@doe-mail.io")
    ids = save_to_sqlite([address])
    print(f"Inserted IDs: {ids}")
