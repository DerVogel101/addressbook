from abc import ABC, abstractmethod
from address import Address

class AddressDatabaseInterface(ABC):
    """
    An abstract base class that defines the interface for an address database.
    """

    @abstractmethod
    def set_path(self, path: str) -> None:
        """
        Sets the path to the database file.

        :param path: The path to the database file.
        :raises TypeError: if the path is invalid
        """
        pass

    @abstractmethod
    def open(self) -> None:
        """
        Opens the database connection.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the database connection.
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """
        Saves the current state of the database.
        """
        pass

    @abstractmethod
    def get_all(self) -> dict[int, Address]:
        """
        Retrieves all addresses from the database.

        :return: A dictionary with address IDs as keys and Address objects as values.
        :rtype: dict[int, Address]
        """
        pass

    @abstractmethod
    def get(self, __id: int) -> Address | None:
        """
        Retrieves an address by its ID.

        :param __id: The ID of the address to retrieve.
        :return: The Address object if found, else None.
        :rtype: Address | None
        """
        pass

    @abstractmethod
    def search(self, search_string: str) -> dict[int, Address]:
        """
        Searches for addresses that match the search string.

        :param search_string: The string to search for.
        :return: A dictionary with address IDs as keys and Address objects as values.
        :rtype: dict[int, Address]
        """
        pass

    @abstractmethod
    def delete(self, __id: int) -> int | None:
        """
        Deletes an address by its ID.

        :param __id: The ID of the address to delete.
        :return: The ID of the deleted address if it was found, else None.
        :rtype: int | None
        """
        pass

    @abstractmethod
    def update(self, __id: int, **kwargs) -> int:
        """
        Updates an address by its ID.

        :param __id: The ID of the address to update.
        :param kwargs: The fields to update.
        :return: The ID of the updated address if it was found.
        :rtype: int
        :raises KeyError: if the address with the given ID does not exist.
        """
        pass

    @abstractmethod
    def add_address(self, address: Address) -> int:
        """
        Adds a new address to the database.

        :param address: The Address object to add.
        :return: The ID of the added address.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_today_birthdays(self) -> dict[int, Address]:
        """
        Retrieves addresses with birthdays today.

        :return: A dictionary with address IDs as keys and Address objects as values.
        :rtype: dict[int, Address]
        """
        pass
