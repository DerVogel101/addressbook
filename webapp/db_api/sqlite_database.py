import sqlite3
from contextlib import closing
from address import Address


def create_table():
    """
    Create the addresses table in the SQLite database if it does not exist.

    This function connects to the SQLite database specified by 'addresses.sqlite3' and creates a table named 'addresses'
    with the following columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - lastname: TEXT
    - firstname: TEXT
    - street: TEXT
    - number: TEXT
    - zip_code: INTEGER
    - city: TEXT
    - birthdate: TEXT
    - phone: TEXT
    - email: TEXT

    The combination of lastname, firstname, street, number, zip_code, city, and birthdate must be unique.
    """
    with closing(sqlite3.connect('addresses.sqlite3')) as conn:
        with conn:
            conn.execute("""
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
            """)


def save_to_sqlite(addresses: list) -> list[int]:
    """
    Save a list of addresses to the SQLite database.

    This function inserts each address in the provided list into the 'addresses' table in the SQLite database.
    If an address already exists (based on the unique constraint), it will be skipped.

    :param addresses: List of Address objects to save
    :type addresses: list
    :return: List of IDs of the inserted addresses
    :rtype: list[int]
    """
    ids = []
    with closing(sqlite3.connect('addresses.sqlite3')) as conn:
        cursor = conn.cursor()
        for address in addresses:
            try:
                cursor.execute("""
                    INSERT INTO addresses (lastname, firstname, street, number, zip_code, city, birthdate, phone, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (address.lastname, address.firstname, address.street, address.number, address.zip_code, address.city, address.birthdate, address.phone, address.email))
                ids.append(cursor.lastrowid)
            except sqlite3.IntegrityError:
                print(f"Duplicate entry found: {address}")
        conn.commit()
    return ids


class SqlitePathError(Exception):
    """
    Exception raised for errors in the SQLite database path.

    This exception is raised when there is an issue with the path to the SQLite database file.
    """
    pass


class SqliteDatabase:
    """
    Class for interacting with an SQLite database.

    This class provides methods to open, close, and interact with an SQLite database specified by the given path.

    :ivar __path: Path to the SQLite database file
    :vartype __path: str
    :ivar __conn: Connection to the SQLite database
    :vartype __conn: sqlite3.Connection | None
    :param path: Path to the SQLite database file
    :type path: str
    """
    def __init__(self, path: str):
        """
        Initialize the SqliteDatabase instance.

        :param path: Path to the SQLite database file
        :type path: str
        """
        self.__path = path
        self.__conn: sqlite3.Connection | None = None

    def open(self):
        """
        Open a connection to the SQLite database.

        This method attempts to open a connection to the SQLite database specified by the path.
        If the database cannot be opened, a SqlitePathError is raised.

        :raises SqlitePathError: If the database cannot be opened
        """
        try:
            self.__conn = sqlite3.connect(self.__path)
        except sqlite3.OperationalError as e:
            raise SqlitePathError(f"Could not open database at {self.__path}") from e
        cursor = self.__conn.cursor()
        cursor.execute("""
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
        """)

    def close(self):
        """
        Close the connection to the SQLite database.

        This method closes the connection to the SQLite database if it is open.
        """
        self.__conn.close()

    def save(self):
        """
        Commit the current transaction to the SQLite database.

        This method commits any pending transaction to the SQLite database.
        """
        self.__conn.commit()

    def add(self, address_obj: Address) -> int:
        """
        Add a new address to the SQLite database.

        This method inserts a new address into the 'addresses' table in the SQLite database.

        :param address_obj: Address object to add
        :type address_obj: Address
        :return: ID of the added address
        :rtype: int
        """
        cursor = self.__conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO addresses (lastname, firstname, street, number, zip_code, city, birthdate, phone, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (address_obj.lastname, address_obj.firstname, address_obj.street, address_obj.number, address_obj.zip_code, address_obj.city, address_obj.birthdate, address_obj.phone, address_obj.email))
        except sqlite3.IntegrityError as e:
            print(f"Invalid entry found: {address_obj}\n"
                  f"{str(e)}")
        return cursor.lastrowid

    def get_where(self, where_clause: str) -> list[dict]:
        """
        Retrieve addresses from the SQLite database that match the given where clause.

        This method executes a SELECT query with the provided where clause and returns the matching addresses.

        :param where_clause: SQL where clause to filter addresses
        :type where_clause: str
        :return: List of dictionaries representing the matching addresses
        :rtype: list[dict]
        """
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(f"SELECT * FROM addresses WHERE {where_clause}")
        result = cursor.fetchall()
        cursor.row_factory = None
        result = [dict(row) for row in result]
        return result

    def get_all(self) -> list[dict]:
        """
        Retrieve all addresses from the SQLite database.

        This method executes a SELECT query to retrieve all addresses from the 'addresses' table.

        :return: List of dictionaries representing all addresses
        :rtype: list[dict]
        """
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("""
            SELECT * FROM addresses
        """)
        result = cursor.fetchall()
        cursor.row_factory = None
        result = [dict(row) for row in result]
        return result

    def delete(self, row_id: int) -> int | None:
        """
        Delete an address from the SQLite database by its ID.

        This method deletes the address with the specified ID from the 'addresses' table.

        :param row_id: ID of the address to delete
        :type row_id: int
        :return: ID of the deleted address if found, else None
        :rtype: int | None
        """
        cursor = self.__conn.cursor()
        cursor.execute("""
            DELETE FROM addresses WHERE id = ?
        """, (row_id,))
        if cursor.rowcount == 1:
            return row_id
        else:
            return None

    def search(self, search_string: str) -> list[dict]:
        """
        Search for addresses in the SQLite database that match the search string.

        This method executes a SELECT query to search for addresses that match the provided search string in any of the
        address fields.

        For more details, see `detailed_sql_search <detailed_sql_search.html>`_.

        :param search_string: String to search for
        :type search_string: str
        :return: List of dictionaries representing the matching addresses
        :rtype: list[dict]
        """
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
        """
        Update an address in the SQLite database by its ID.

        This method updates the address with the specified ID in the 'addresses' table with the provided fields.

        :param row_id: ID of the address to update
        :type row_id: int
        :param kwargs: Fields to update
        :return: ID of the updated address if found, else None
        :rtype: int | None
        """
        try:
            previous = self.get_where(f"id = {row_id}")[0]
        except IndexError:
            return None
        previous.update(kwargs)
        cursor = self.__conn.cursor()
        cursor.execute("""
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
        """, (previous['lastname'], previous['firstname'], previous['street'], previous['number'], previous['zip_code'], previous['city'], previous['birthdate'], previous['phone'], previous['email'], row_id))
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