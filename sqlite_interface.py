from typing import Optional

from address_container_interface import AddressDatabaseInterface
from sqlite_database import SqliteDatabase, SqlitePathError
from address import Address
from datetime import date


class SqliteInterface(AddressDatabaseInterface):
    """
    Interface for interacting with an SQLite database containing address information.

    :ivar __sql_path: Path to the SQLite database file.
    :vartype __sql_path: str | None
    :ivar __squirrel_lite: SQLite database object.
    :vartype __squirrel_lite: SqliteDatabase | None
    :ivar __connection_open: Flag indicating whether the database connection is open.
    :vartype __connection_open: bool
    :param path: Optional path to the SQLite database file.
    :type path: str, optional
    """
    def __init__(self, path: Optional[str] = None):
        """
        Initialize the SqliteInterface instance.

        :param path: Optional path to the SQLite database file.
        :type path: str, optional
        """
        self.__sql_path: str | None = path
        self.__squirrel_lite: SqliteDatabase | None = None
        self.__connection_open = False

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object.

        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Traceback object
        """
        if self.__squirrel_lite:
            self.__squirrel_lite.close()
            self.__squirrel_lite = None
        self.__connection_open = False

    def __iter__(self) -> iter:
        """
        Return an iterator over all addresses in the database.

        :return: Iterator of tuples containing (id, Address)
        :rtype: iter
        """
        data = self.get_all()
        result_iter = [(key, data[key]) for key in data].__iter__()
        return result_iter

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.__exit__(None, None, None)

    def set_path(self, path: str) -> None:
        """
        Set the path to the SQLite database file.

        :param path: Path to the SQLite database file
        :type path: str
        :raises TypeError: If the path is not a string
        :raises ValueError: If the connection is open
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        if not self.__connection_open:
            self.__sql_path = path
        else:
            raise ValueError("Connection is open") from SqlitePathError("Cannot set path while connection is open")

    def open(self) -> None:
        """
        Open the database connection.

        :raises ValueError: If the path is invalid
        """
        if not self.__sql_path:
            raise ValueError("Path is not set") from SqlitePathError("Invalid path")
        self.__squirrel_lite = SqliteDatabase(self.__sql_path)
        try:
            self.__squirrel_lite.open()
            self.__connection_open = True
        except SqlitePathError as e:
            raise ValueError(f"Could not open database at {self.__sql_path}") from e

    def save(self) -> None:
        """
        Save changes to the database.
        """
        self.__squirrel_lite.save()

    def get_all(self) -> dict[int, Address]:
        """
        Retrieve all addresses from the database.

        :return: Dictionary of addresses with their IDs as keys
        :rtype: dict[int, Address]
        :raises ValueError: If the database is not open
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_all()
        return {row['id']: Address(**row) for row in cursor}

    def get(self, __id: int) -> Address | None:
        """
        Retrieve an address by its ID.

        :param __id: ID of the address
        :type __id: int
        :return: Address object if found, else None
        :rtype: Address | None
        :raises ValueError: If the database is not open
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_where(f"id = {__id}")
        if cursor:
            return Address(**cursor[0])
        return None

    def search(self, search_string: str) -> dict[int, Address]:
        """
        Search for addresses matching the search string.

        :param search_string: String to search for
        :type search_string: str
        :return: Dictionary of matching addresses with their IDs as keys
        :rtype: dict[int, Address]
        :raises ValueError: If the database is not open
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_search = self.__squirrel_lite.search(search_string)
        return {row['id']: Address(**row) for row in result_search}

    def delete(self, __id: int) -> int | None:
        """
        Delete an address by its ID.

        :param __id: ID of the address to delete
        :type __id: int
        :return: ID of the deleted address if found, else None
        :rtype: int | None
        :raises ValueError: If the database is not open
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_status = self.__squirrel_lite.delete(__id)
        return result_status

    def update(self, __id: int, **kwargs) -> int:
        """
        Update an address by its ID.

        :param __id: ID of the address to update
        :type __id: int
        :param kwargs: Fields to update
        :return: ID of the updated address if found, else None
        :rtype: int
        :raises ValueError: If the database is not open
        :raises KeyError: If the address with the given ID does not exist
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_status = self.__squirrel_lite.update(__id, **kwargs)
        if result_status is None:
            raise KeyError(f"Address with id {__id} not found")
        return result_status

    def add_address(self, address) -> int:
        """
        Add a new address to the database.

        :param address: Address object to add
        :type address: Address
        :return: ID of the added address
        :rtype: int
        :raises TypeError: If the address is not an instance of Address
        :raises ValueError: If the database is not open
        """
        if not isinstance(address, Address):
            raise TypeError("Address must be an instance of Address")
        row_id = self.__squirrel_lite.add(address)
        return row_id

    def get_todays_birthdays(self) -> dict[int, Address]:
        """
        Retrieve addresses with birthdays today.

        :return: Dictionary of addresses with their IDs as keys
        :rtype: dict[int, Address]
        :raises ValueError: If the database is not open
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_where(f"strftime('%m-%d', birthdate) = '{date.today().strftime('%m-%d')}'")
        return {row['id']: Address(**row) for row in cursor}