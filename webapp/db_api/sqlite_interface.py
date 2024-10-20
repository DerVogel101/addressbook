from typing import Optional

from .address_container_interface import AddressDatabaseInterface
from .sqlite_database import SqliteDatabase, SqlitePathError
from .address import Address
from datetime import date


class SqliteInterface(AddressDatabaseInterface):
    def __init__(self, path: Optional[str] = None):
        self.__sql_path: str | None = path
        self.__squirrel_lite: SqliteDatabase | None = None
        self.__connection_open = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__squirrel_lite:
            self.__squirrel_lite.close()
            self.__squirrel_lite = None
        self.__connection_open = False

    def __iter__(self) -> iter:
        data = self.get_all()
        result_iter = [(key, data[key]) for key in data].__iter__()
        return result_iter

    def close(self) -> None:
        self.__exit__(None, None, None)

    def set_path(self, path: str) -> None:
        """
        :raises TypeError: if the path is not a string
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        if not self.__connection_open:
            self.__sql_path = path
        else:
            raise ValueError("Connection is open") from SqlitePathError("Cannot set path while connection is open")

    def open(self) -> None:
        """
        :raises ValueError: if the path is invalid
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
        self.__squirrel_lite.save()

    def get_all(self) -> dict[int: Address]:
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_all()
        return {row['id']: Address(**row) for row in cursor}

    def get(self, __id: int) -> Address | None:
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_where(f"id = {__id}")
        if cursor:
            return Address(**cursor[0])
        return None

    def search(self, search_string: str) -> dict[int: Address]:
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_search = self.__squirrel_lite.search(search_string)
        return {row['id']: Address(**row) for row in result_search}

    def delete(self, __id: int) -> int | None:
        """:return: the id of the deleted address if it was found, else None"""
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_status = self.__squirrel_lite.delete(__id)
        return result_status

    def update(self, __id: int, **kwargs) -> int:
        """
        :return: the id of the updated address if it was found, else None
        :raises KeyError: if the address with the given id does not exist
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_status = self.__squirrel_lite.update(__id, **kwargs)
        if result_status is None:
            raise KeyError(f"Address with id {__id} not found")
        return result_status

    def add_address(self, address) -> int:
        """:return: the id of the added address"""
        if not isinstance(address, Address):
            raise TypeError("Address must be an instance of Address")
        row_id = self.__squirrel_lite.add(address)
        return row_id

    def get_today_birthdays(self) -> dict[int: Address]:
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        cursor = self.__squirrel_lite.get_where(f"birthdate = '{date.today()}'")
        return {row['id']: Address(**row) for row in cursor}


if __name__ == "__main__":
    pass
