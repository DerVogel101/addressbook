import os

from address_container_interface import AddressDatabaseInterface
from sqlite_database import SqliteDatabase
from address import Address
from datetime import date


class SqliteInterface(AddressDatabaseInterface):
    def __init__(self):
        self.__sql_path: str | None = None
        self.__squirrel_lite: SqliteDatabase | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__squirrel_lite:
            self.__squirrel_lite.close()
            self.__squirrel_lite = None

    def set_path(self, path: str) -> None:
        """
        :raises TypeError: if the path is invalid
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        self.__sql_path = path

    def open(self) -> None:
        """
        :raises ValueError: if the path is invalid
        """
        if not self.__sql_path:
            raise ValueError("Path is not set")
        self.__squirrel_lite = SqliteDatabase(self.__sql_path)

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

    def update(self, __id: int, **kwargs) -> int | None:
        """
        :return: the id of the updated address if it was found, else None
        :raises KeyError: if the address with the given id does not exist
        """
        if not self.__squirrel_lite:
            raise ValueError("Database is not open")
        result_status = self.__squirrel_lite.update(__id, **kwargs)
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
    from context_support import ContextSupport

    with ContextSupport(SqliteInterface()) as adress_book:
        adress_book.set_path("addresses.sqlite3")
        adress_book.open()
        # adress_book.add_address(Address(
        #     lastname="Günther", firstname="Harald", street="Main.cpp", number="-1", zip_code=404,
        #     city="Gravity Falls", birthdate="1990-01-01", phone="+49 176 1234 5678",
        #     email="anomaly@krampf.xd"
        # ))
        id1 = adress_book.add_address(Address(
            lastname="Gunther", firstname="Hari", street="Main.cpp", number="-1", zip_code=404,
            city="Gravity Falls", birthdate="2024-09-07", phone="+49 176 1234 5678",
            email="anomaly@krampf.xd"
        ))
        id2 = adress_book.add_address(Address(
            lastname="Gunther", firstname="Häri", street="Main.cpp", number="-1", zip_code=404,
            city="Gravity Falls", birthdate="2024-09-07", phone="+49 176 1234 5678",
            email="anomaly@krampf.xd"
        ))
        print("Added: ", id1, id2)
        delete_id1 = adress_book.delete(id1)
        delete_id2 = adress_book.delete(id2)
        print("Deleted:", delete_id1, delete_id2)
        result = adress_book.get_today_birthdays()
        print("Got Birthdays Today:", result)
        result = adress_book.get(73)
        print("Got Address 73:", result)
        result = adress_book.get_all()
        print("Got All:", result)
        result = adress_book.search("John")
        print("Searched for John:", result)
        before = adress_book.get(1)
        result = adress_book.update(1, lastname="Doe", email=None)
        after = adress_book.get(1)
        print("Updated 1 to Doe:", result)
        print("Before:", before)
        print("After:", after)
        # adress_book.save()
